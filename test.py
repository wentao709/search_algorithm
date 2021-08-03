import time

def main():
    start_time = time.time()
    s = ['5','5', '6']
    i = [int(s[0]), int(s[1]), int(s[2])]
    end = time.time()
    print("--- %s seconds ---" % (end - start_time))
main()
