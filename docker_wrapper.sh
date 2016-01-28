#!/bin/sh
set -eu
imagename=luajitrpm

usage() {
  cat <<'EOF' 1>&2
Usage: docker_wrapper.sh subcommand args...

subcommands:
  build            build the docker image with tag "$imagename"
  run              run the docker image of tag "$imagename"
  bash             run /bin/bash in the docker image of tag "$imagename"
EOF
}

case "${1:-}" in
build)
  docker build -t $imagename .
  ;;
run)
  # NOTE: The following error occurred when I tried with --cap-add=SYS_ADMIN instead of --privileged=true.
  # ---------------------------------------------------------------------------------------------------------
  # Failed:
  #   filesystem.x86_64 0:3.2-20.el7
  #   glibc-common.x86_64 0:2.17-106.el7_2.1
  # 
  # Complete!
  # ERROR: Command failed. See logs for output.
  #    # /usr/bin/yum --installroot /var/lib/mock/epel-7-x86_64/root/ --releasever 7 install @buildsys-build
  # ---------------------------------------------------------------------------------------------------------
  # I use --privileged=true for now since I don't know how to figure which capabilities are needed.
  docker run --privileged=true -e "COPR_LOGIN=$COPR_LOGIN" -e "COPR_USERNAME=$COPR_USERNAME" -e "COPR_TOKEN=$COPR_TOKEN" -it $imagename
  ;;
bash)
  # NOTE: The following error occurred when I tried with --cap-add=SYS_ADMIN instead of --privileged=true.
  # ---------------------------------------------------------------------------------------------------------
  # Failed:
  #   filesystem.x86_64 0:3.2-20.el7
  #   glibc-common.x86_64 0:2.17-106.el7_2.1
  # 
  # Complete!
  # ERROR: Command failed. See logs for output.
  #    # /usr/bin/yum --installroot /var/lib/mock/epel-7-x86_64/root/ --releasever 7 install @buildsys-build
  # ---------------------------------------------------------------------------------------------------------
  # I use --privileged=true for now since I don't know how to figure which capabilities are needed.
  docker run --privileged=true -e "COPR_LOGIN=$COPR_LOGIN" -e "COPR_USERNAME=$COPR_USERNAME" -e "COPR_TOKEN=$COPR_TOKEN" -it $imagename /bin/bash
  ;;
*)
  usage
  ;;
esac
