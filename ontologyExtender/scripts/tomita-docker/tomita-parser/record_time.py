import subprocess
import time


def main():
    start_time = time.time()
    print("Preparing to run Tomita parser...")

    # run command tomita-parser tomita-parser/proto/config.proto
    subprocess.call(["tomita-parser", "proto/config.proto"])

    print("Tomita parser finished in {} seconds".format(time.time() - start_time))


if __name__ == '__main__':
    main()