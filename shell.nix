
{ pkgs ? import <nixpkgs> {} }:

let 

  mypython = pkgs.python37;

  project-pkgs = python-packages: with python-packages;
  [
    # core
    click requests 
    # dev
    jedi mypy 
  ];

  python-env = mypython.withPackages (project-pkgs);

in 
with pkgs;
mkShell {

  buildInputs = [ python-env ];

  shellHook = ''
    rm -f env
    ln -s ${python-env}/bin env
  '';

}
