# Pre-baked image for the Learn video gate (.github/workflows/video-ci.yml).
#
# The gate re-downloaded the SAME predictable dependencies on every push to every video PR:
# chromium + fonts (apt), the pinned hyperframes CLI (npx), and chrome-headless-shell
# (`browser ensure`). This image bakes all of it so the gate job only runs the checks.
#
# Rebuild ONLY when HYPERFRAMES_VERSION changes (keep it in lockstep with
# learn/config.json -> cli.published_version). The build-ci-image workflow does that + smoke-tests
# the result before it is ever used by the gate.
FROM node:22-bookworm-slim

ARG HYPERFRAMES_VERSION=0.7.77
ENV HYPERFRAMES_VERSION=${HYPERFRAMES_VERSION}
ENV DEBIAN_FRONTEND=noninteractive
# `hyperframes browser ensure` downloads chrome-headless-shell to 100% but then never exits in the
# buildkit sandbox (spinner/keep-alive holds the event loop). The binary is on disk by then, so cap
# it, swallow the timeout kill, and let the find/test below be the real success check.
ENV CI=1 NO_COLOR=1

# python (the check_*.py tools call `python`, so alias python->python3), chromium for the ABI/libs
# the headless-shell needs, fallback fonts (Segoe is NOT needed — the gates are colour/structure,
# brand-final render is a separate Windows job), and git/ca-certs for actions/checkout.
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python-is-python3 \
      chromium \
      fontconfig fonts-liberation fonts-noto-core fonts-dejavu-core \
      git ca-certificates \
    && fc-cache -f \
    && rm -rf /var/lib/apt/lists/*

# hyperframes CLI pinned + global, and chrome-headless-shell provisioned INTO the image at a fixed
# path. GitHub container jobs override HOME (=/github/home), so a cache under /root would be lost at
# runtime — resolve the binary now and pin it via HYPERFRAMES_CHROME_PATH, which survives the HOME
# override. (Chrome finds its resources relative to the real binary, so a symlink is safe.)
RUN npm install -g "hyperframes@${HYPERFRAMES_VERSION}" \
    && (timeout -k 10 300 hyperframes browser ensure || true) \
    && CHS="$(find / -type f -name 'chrome-headless-shell' 2>/dev/null | head -1)" \
    && test -n "$CHS" \
    && ln -sf "$CHS" /usr/local/bin/chrome-headless-shell \
    && npm cache clean --force
ENV HYPERFRAMES_CHROME_PATH=/usr/local/bin/chrome-headless-shell

WORKDIR /work
