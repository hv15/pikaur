#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

new_version=$1

if [[ $(git status --porcelain 2>/dev/null| grep "^ [MD]" | wc -l) -gt 0 ]] ; then
	echo "You have uncommited changes"
	git status
	exit 1
fi

sed -i -e "s/pkgver=.*/pkgver=${new_version}/g" PKGBUILD
sed -i -e "s/VERSION.*=.*/VERSION = '${new_version}'/g" pikaur/config.py
git commit -am "chore: bump version to ${new_version}"
git tag -a "${new_version}"
