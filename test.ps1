# use this to run test suite on windows hosts

docker build -t salusfy .

docker run -it -v .:/app salusfy