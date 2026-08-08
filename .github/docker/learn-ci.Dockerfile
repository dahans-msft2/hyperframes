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
ENV CI=1 NO_COLOR=1

# python (the check_*.py tools call `python`, so alias python->python3), chromium for the ABI/libs
# the headless-shell needs, fallback fonts (Segoe is NOT needed — the gates are colour/structure,
# brand-final render is a separate Windows job), and git/ca-certs for actions/checkout.
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python-is-python3 \
      chromium \
      fontconfig fonts-liberation fonts-noto-core fonts-dejavu-core \
      git ca-certificates unzip \
    && fc-cache -f \
    && rm -rf /var/lib/apt/lists/*

# hyperframes CLI pinned + global, and chrome-headless-shell provisioned INTO the image at a fixed
# path. GitHub container jobs override HOME (=/github/home), so a cache under /root would be lost at
# runtime — resolve the binary now and pin it via HYPERFRAMES_CHROME_PATH, which survives the HOME
# override. (Chrome finds its resources relative to the real binary, so a symlink is safe.)
# hyperframes' downloader needs `unzip` (installed above) to extract chrome-headless-shell; without it
# the download reaches 100% then fails extraction. The timeout is a hang safety net.
RUN npm install -g "hyperframes@${HYPERFRAMES_VERSION}" \
    && timeout 600 hyperframes browser ensure \
    && CHS="$(find / -type f -name 'chrome-headless-shell' 2>/dev/null | head -1)" \
    && test -n "$CHS" \
    && ln -sf "$CHS" /usr/local/bin/chrome-headless-shell \
    && npm cache clean --force
ENV HYPERFRAMES_CHROME_PATH=/usr/local/bin/chrome-headless-shell

WORKDIR /work
