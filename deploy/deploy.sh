#!/bin/sh
# Deploy one commit of main on this host. Run by CI over SSH as a forced command:
# authorized_keys pins the deploy key to this script, and the client's requested "command" arrives
# in $SSH_ORIGINAL_COMMAND, which must be a full commit hash that is already on origin/main.
#
# Everything runs inside main() so the whole file is parsed before `git checkout` can replace it.
set -eu

main() {
    cd "$(dirname "$0")/.."

    sha="${SSH_ORIGINAL_COMMAND:-${1:-}}"
    if ! printf '%s' "$sha" | grep -Eq '^[0-9a-f]{40}$'; then
        echo "deploy: expected a 40-character commit hash, refusing" >&2
        exit 2
    fi

    git fetch --quiet origin main
    if ! git merge-base --is-ancestor "$sha" origin/main 2>/dev/null; then
        echo "deploy: $sha is not on origin/main, refusing" >&2
        exit 3
    fi

    echo "deploy: $(git log -1 --format='%h %s' "$sha")"
    git checkout --quiet --detach "$sha"
    docker compose up -d --build --remove-orphans

    echo "deploy: waiting for /healthz/"
    for _ in $(seq 1 24); do
        if curl -fsS -H 'X-Forwarded-Proto: https' http://127.0.0.1:8000/healthz/ >/dev/null 2>&1; then
            echo "deploy: healthy at $(git rev-parse --short HEAD)"
            docker image prune -f >/dev/null
            exit 0
        fi
        sleep 5
    done

    echo "deploy: app did not become healthy within 2 minutes" >&2
    docker compose logs --tail 50 web >&2
    exit 1
}

main "$@"
# Never read past this line, even if the checkout rewrote the file while it was running.
# shellcheck disable=SC2317
exit
