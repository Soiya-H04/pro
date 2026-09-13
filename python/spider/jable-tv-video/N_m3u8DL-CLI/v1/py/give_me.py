"""

顶层模块

"""

from aux_module import *
from build_struct import *
from downloader_v1 import *


if __name__ == '__main__':
    # 构建项目
    clean_cmd()
    write_out("build program....", move_cursor(1))
    paths = create_all()
    write_out("done")

    # 创建下载器并完成相应初始化
    d = DownLoader(paths)

    # 进入初始界面
    time.sleep(1)
    clean_cmd()

    # 进入程序循环
    option1 = choice_interface()
    while True:
        if option1 == "add":
            d.add_video()

            return_count(3)
            clean_cmd()

            option1 = choice_interface()

        elif option1 == "check":
            clean_cmd()

            option2 = check_interface()
            while True:
                if option2 == "config":
                    while True:
                        clean_cmd()

                        print_config(d.config)

                        write_out("type exit to return: ", move_cursor(1))
                        option3 = read_in()

                        if option3 == "exit":
                            clean_cmd()
                            option2 = check_interface()
                            break
                        else:
                            write_out("type wrong!", move_cursor(1))
                            write_out("please type exit.", move_cursor(1))
                            return_count(3)

                elif option2 == "video":
                    while True:
                        clean_cmd()

                        print_video(d.video)

                        write_out("type exit to return: ", move_cursor(1))
                        option3 = read_in()
                        if option3 == "exit":
                            clean_cmd()
                            option2 = check_interface()

                            break
                        else:
                            write_out("type wrong!", move_cursor(1))
                            write_out("please type exit.", move_cursor(1))
                            return_count(3)

                elif option2 == "new_video":
                    while True:
                        clean_cmd()

                        print_new_video(d.new_video)

                        write_out("type exit to return: ", move_cursor(1))
                        option3 = read_in()
                        if option3 == "exit":
                            clean_cmd()
                            option2 = check_interface()

                            break
                        else:
                            write_out("type wrong!", move_cursor(1))
                            write_out("please type exit.", move_cursor(1))
                            return_count(3)

                elif option2 == "exit":
                    clean_cmd()
                    option1 = choice_interface()

                    break

                else:
                    write_out("choice maybe go wrong!", move_cursor(1))
                    write_out("please choose again.", move_cursor(1))
                    return_count(3)

                    clean_cmd()
                    option2 = check_interface()

        elif option1 == "sdl" or option1 == "start download":
            d.start_download()

            while True:
                clean_cmd()
                write_out("download finished.", move_cursor(1))
                write_out("type exit to return: ", move_cursor(1))

                option4 = read_in()
                if option4 == "exit":
                    clean_cmd()
                    option1 = choice_interface()
                    break

                else:
                    write_out("type wrong!", move_cursor(1))
                    write_out("please type exit.", move_cursor(1))
                    return_count(3)

        elif option1 == "exit":
            clean_cmd()
            write_out("program finished.", move_cursor(1))
            break

        else:
            write_out("choice maybe go wrong!", move_cursor(1))
            write_out("please choose again.", move_cursor(1))
            return_count(3)
            clean_cmd()
            option1 = choice_interface()
