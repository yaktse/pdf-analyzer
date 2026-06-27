{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    nodejs_22
  ];

  shellHook = ''
    echo "Node.js environment loaded"
    echo "Node: $(node --version)"
    echo "NPM:  $(npm --version)"
  '';
}
