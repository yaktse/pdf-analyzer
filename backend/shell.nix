{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    python312
    python312Packages.pip
    python312Packages.virtualenv

    gcc
    stdenv.cc.cc.lib
  ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.stdenv.cc.cc.lib
  ];

  shellHook = ''
    echo "Python environment loaded."

    if [ ! -d .venv ]; then
      python -m venv .venv
    fi

    source .venv/bin/activate
  '';
}
