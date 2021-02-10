import argparse
import sys
import spotify
import new_gmusic
import local
def main(argv):

    parser = argparse.ArgumentParser(
        description="Move your playlist on Spotify")
    parser.add_argument(
        "-m", "--mode", required=True, metavar='convert_mode',
        help="Specify convert mode:\n gp: for google play music,\n f to take from folders", type=str, default="gp")
    parser.add_argument(
        "-p", "--path", required=False, metavar='folder_path',
        help="Path where the folder are stored", type=str, default="gp")

    args = vars(parser.parse_args())
    convert_mode = args['mode']
    folder_path = args['path']
    if convert_mode=="gp":
        print("Converting csv...")
        new_gmusic.print_playlists()
        print("\nStart ...")
        spotify.main()
    elif convert_mode=="f":
        print("Converting local...")
        local.main_local(path=folder_path)

    print("Completed!\n")


if __name__ == "__main__":
    main(sys.argv[1:])