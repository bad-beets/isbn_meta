{ lib, python3Packages }:
with python3Packages;
buildPythonApplication {
  pname = "isbn_meta";
  version = "0.69";

  propagatedBuildInputs = [ fuzzywuzzy
                            hypothesis
                            pint
                            sqlalchemy
                            configparser
                            pandas
                            numpy
                            requests
                            pytest
                          ];

  src = ./.;
}
