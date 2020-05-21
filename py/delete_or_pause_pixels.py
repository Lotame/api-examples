'''
    Please note that this file is an example, not an official Lotame-supported
    tool. The Support team at Lotame does not provide support for this script,
    as it's only meant to serve as a guide to help you use the Services API.

    Filename: delete_or_pause_pixels.py
    Author: Brett Coker
    Python Version: 3.6.1

    Takes a .txt file containing pixel IDs as an argument. One pixel ID per
    line.

    Deletes or pauses pixels. The endpoint is the same for either task, so what
    actually happens depends on the pixel itself (broadcasters get paused,
    others get deleted).
'''
import sys
import better_lotameapi


def main():
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} pixel_ids.txt')
        return

    lotame = better_lotameapi.Lotame()

    filename = sys.argv[1]
    with open(filename) as pixel_ids:
        for pixel_id in pixel_ids:
            pixel_id = pixel_id.strip()

            status = lotame.delete(f'pixels/{pixel_id}').status_code

            if status == 204:
                print(f'Deleted/paused pixel {pixel_id}')
            else:
                print(f'Could not delete/pause pixel {pixel_id}')

    
if __name__ == '__main__':
    main()
