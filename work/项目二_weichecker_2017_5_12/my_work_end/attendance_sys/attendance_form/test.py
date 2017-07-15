# coding=utf8


if __name__ == "__main__":
    stus = []
    while 1:
        name = raw_input("姓名：")
        if name:
            stus.append(name)
        else:
            break

    print stus