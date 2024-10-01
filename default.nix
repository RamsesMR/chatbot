{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # Especificar las dependencias de sistema necesarias
  buildInputs = [
    pkgs.python310       # Versión de Python que deseas usar
    pkgs.python310Packages.pip   # Pip para instalar dependencias
    pkgs.python310Packages.venv  # Crear entornos virtuales si es necesario
    pkgs.gunicorn        # Servidor Gunicorn para Flask
    pkgs.pkgconfig       # A veces necesario para compilar paquetes
    pkgs.gcc             # Necesario para compilar algunos módulos de Python
  ];

  # El comando para ejecutar la aplicación, si es necesario en el build
  shellHook = ''
    # Crear el entorno virtual de Python
    python3 -m venv venv
    source venv/bin/activate

    # Instalar las dependencias del archivo requirements.txt
    pip install -r requirements.txt
  '';
}