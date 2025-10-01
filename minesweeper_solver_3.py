import tkinter as tk

m = int(input("Enter the number of rows: "))
n = int(input("Enter the number of columns: "))
mine_total = int(input("Enter the number of mines: "))

state_list = []
entry_list = []
stringvar_list = []

def cal_prob():
    print('-' * 20)
    out = True
    for i in range((n + 2) * (m + 2)):
        state_list[i] = entry_list[i].get()
        entry_list[i]['foreground'] = 'black'
        entry_list[i]['background'] = 'white'
        if state_list[i] == '-1':
            entry_list[i]['background'] = 'yellow'
        elif state_list[i] == '':
            entry_list[i]['background'] = 'cyan'
        elif state_list[i] == '0':
            entry_list[i]['foreground'] = 'black'
        elif state_list[i] == '1':
            entry_list[i]['foreground'] = 'blue'
        elif state_list[i] == '2':
            entry_list[i]['foreground'] = 'green'
        elif state_list[i] == '3':
            entry_list[i]['foreground'] = 'orange'
        elif state_list[i] == '4':
            entry_list[i]['foreground'] = 'purple'
        else:
            entry_list[i]['foreground'] = 'red'

    count_list_list = []
    num_list = []

    # 平凡情况判断
    for i in range(m):
        for j in range(n):
            state = state_list[n + 3 + j + (n + 2) * i]
            # ''表示未知，'0'表示空位，'-1'表示雷，'2~8'表示周围雷数
            if state != '' and state != '0' and state != '-1':
                # 收集该数字格周围剩余的雷数与空格数
                num = int(state)
                count = 0
                count_list = []
                for s in range(3):
                    for t in range(3):
                        if state_list[(n + 2) * s + t + j + (n + 2) * i] == '':
                            count += 1
                            count_list.append((n + 2) * s + t + j + (n + 2) * i)
                        if state_list[(n + 2) * s + t + j + (n + 2) * i] == '-1':
                            num -= 1

                if num == 0 and count != 0:
                    out = False
                    for place in count_list:
                        entry_list[place]['background'] = 'green'
                if num == count and num != 0:
                    out = False
                    for place in count_list:
                        entry_list[place]['background'] = 'red'
                        stringvar_list[place].set('-1')

                if num != 0 and num != count:
                    count_list_list.append(count_list)
                    num_list.append(num)

                if num > count or num < 0:
                    print('{}行{}列报错'.format(i + 1, j + 1))
                    entry_list[n + 3 + j + (n + 2) * i]['background'] = 'purple'

    stop = False
    num_list_save = []
    count_list_list_save = []

    # 多级判断
    while not stop:
        stop = True
        save_list = []
        for i in range(len(num_list)):
            save_list.append(True)
        for i in range(len(num_list)):

            # 一定要这个判断，不然会爆炸，经典情形4~6~15~105~5460~14903070
            if save_list[i] == True:

                # 平凡情况的自检
                if num_list[i] == 0:
                    save_list[i] = False
                    for place in count_list_list[i]:
                        entry_list[place]['background'] = 'green'
                if num_list[i] == len(count_list_list[i]):
                    save_list[i] = False
                    for place in count_list_list[i]:
                        entry_list[place]['background'] = 'red'
                        stringvar_list[place].set('-1')

                # 互检
                for j in range(i + 1, len(num_list)):
                    only_i = []
                    only_j = []
                    i_and_j = []

                    # 提取出i和j中重复出现的和单独具有的格子
                    for place in count_list_list[i]:
                        if place in count_list_list[j]:
                            i_and_j.append(place)
                        else:
                            only_i.append(place)
                    for place in count_list_list[j]:
                        if not place in i_and_j:
                            only_j.append(place)

                    # 两种可确定有雷和没雷的情况
                    if num_list[j] - len(only_j) == num_list[i]:
                        stop = False
                        save_list[i] = False
                        save_list[j] = False
                        num_list_save.append(num_list[i])
                        count_list_list_save.append(i_and_j)
                        if len(only_i) != 0 or len(only_j) != 0:
                            out = False
                        for place in only_i:
                            entry_list[place]['background'] = 'green'
                        for place in only_j:
                            entry_list[place]['background'] = 'red'
                            stringvar_list[place].set('-1')

                    elif num_list[i] - len(only_i) == num_list[j]:
                        stop = False
                        save_list[i] = False
                        save_list[j] = False
                        num_list_save.append(num_list[j])
                        count_list_list_save.append(i_and_j)
                        if len(only_i) != 0 or len(only_j) != 0:
                            out = False
                        for place in only_j:
                            entry_list[place]['background'] = 'green'
                        for place in only_i:
                            entry_list[place]['background'] = 'red'
                            stringvar_list[place].set('-1')

                    # 两种可化简的情况
                    elif len(only_i) == 0 and len(only_j) != 0 and len(i_and_j) != 0:
                        stop = False
                        save_list[i] = False
                        save_list[j] = False
                        num_list_save.append(num_list[i])
                        count_list_list_save.append(i_and_j)
                        num_list_save.append(num_list[j] - num_list[i])
                        count_list_list_save.append(only_j)

                    elif len(only_j) == 0 and len(only_i) != 0 and len(i_and_j) != 0:
                        stop = False
                        save_list[i] = False
                        save_list[j] = False
                        num_list_save.append(num_list[j])
                        count_list_list_save.append(i_and_j)
                        num_list_save.append(num_list[i] - num_list[j])
                        count_list_list_save.append(only_i)

            if save_list[i] == True:
                num_list_save.append(num_list[i])
                count_list_list_save.append(count_list_list[i])

        count_list_list = []
        num_list = []
        for i in range(len(num_list_save)):
            count_list_list.append(count_list_list_save[i])
            num_list.append(num_list_save[i])
        num_list_save = []
        count_list_list_save = []

    # 剩余雷数判断
    if out == True:
        mine_exist = 0
        for i in range((n + 2) * (m + 2)):
            if state_list[i] == '-1':
                mine_exist += 1
        mine_remaining = mine_total - mine_exist

        # 提取完全无关的未知格子
        other_list = []
        for i in range(m):
            for j in range(n):
                state = state_list[n + 3 + j + (n + 2) * i]
                if state == '':
                    other = True
                    for s in range(3):
                        for t in range(3):
                            if (state_list[(n + 2) * s + t + j + (n + 2) * i] != ''
                                    and state_list[(n + 2) * s + t + j + (n + 2) * i] != '0'
                                    and state_list[(n + 2) * s + t + j + (n + 2) * i] != '-1'):
                                other = False
                    if other == True:
                        other_list.append(n + 3 + j + (n + 2) * i)

        # 提取相关的未知格子
        total_count_list = []
        for i in range(len(num_list)):
            for place in count_list_list[i]:
                if not place in total_count_list:
                    total_count_list.append(place)

        # 暴力枚举可能的解
        mine_max = 0
        mine_min = len(total_count_list)
        mine_list_list = []
        mine_list_index_list = []

        x_list_list = []
        x_max_list_list = []
        x_min_list_list = []


        for i in range(len(num_list)):
            x_list = []
            x_max_list = []
            x_min_list = []
            for j in range(num_list[i]):
                x_list.append(num_list[i] - j - 1)
                x_max_list.append(len(count_list_list[i]) - j - 1)
                x_min_list.append(num_list[i] - j - 1)
            x_list_list.append(x_list)
            x_max_list_list.append(x_max_list)
            x_min_list_list.append(x_min_list)
        # print(x_max_list_list)
        # print(x_min_list_list)

        x_max = 1
        for i in range(len(num_list)):
            for j in range(num_list[i]):
                x_max *= len(count_list_list[i]) - j
                x_max /= j + 1
        x_max = int(x_max)
        # print(x_max)


        for i in range(x_max):
            stop = False
            correct = True
            mine_list = []

            for j in range(len(num_list)):
                if not stop:
                    for k in range(num_list[j]):
                        if x_list_list[j][k] > x_max_list_list[j][k]:
                            if k == num_list[j] - 1:
                                for l in range(len(x_list_list[j])):
                                    x_list_list[j][l] = x_min_list_list[j][l]
                                x_list_list[j + 1][0] += 1
                            else:
                                x_list_list[j][k + 1] += 1
                                if x_list_list[j][k + 1] <= x_max_list_list[j][k + 1]:
                                    for l in range(k + 1):
                                        x_list_list[j][l] = x_list_list[j][k + 1] + k + 1 - l
                                    stop = True
                                    break
                        else:
                            stop = True
                            break
                else:
                    break
            # print(x_list_list)


            for j in range(len(num_list)):
                for k in range(num_list[j]):
                    if not count_list_list[j][x_list_list[j][k]] in mine_list:
                        mine_list.append(count_list_list[j][x_list_list[j][k]])

            if correct == True:
                for j in range(len(num_list)):
                    num = 0
                    for place in count_list_list[j]:
                        if place in mine_list:
                            num += 1
                    if num != num_list[j]:
                        correct = False
                        break

            if correct == True:
                mine_list_index = []
                for j in range(len(total_count_list)):
                    if not total_count_list[j] in mine_list:
                        mine_list_index.append(0)
                    else:
                        mine_list_index.append(1)
                if not mine_list_index in mine_list_index_list:
                    mine_list_list.append(mine_list)
                    mine_list_index_list.append(mine_list_index)
                if len(mine_list) < mine_min:
                    mine_min = len(mine_list)
                if len(mine_list) > mine_max:
                    mine_max = len(mine_list)

            x_list_list[0][0] += 1

        # print(mine_list_list)

        # 两种可以确定无关未知格子状态的情况
        if mine_min == mine_remaining and len(other_list) != 0:
            for place in other_list:
                out = False
                entry_list[place]['background'] = 'green'
        elif mine_max + len(other_list) == mine_remaining and len(other_list) != 0:
            for place in other_list:
                out = False
                entry_list[place]['background'] = 'red'
                stringvar_list[place].set('-1')

        # 对其中可能的情况进行重叠以确定未知格子状态
        else:
            mine_list_list_possible = []
            for place in total_count_list:
                unsafe = True
                safe = True
                for j in range(len(mine_list_list)):
                    if (len(mine_list_list[j]) <= mine_remaining
                            and len(mine_list_list[j]) >= mine_remaining - len(other_list)):
                        mine_list_list_possible.append(mine_list_list[j])
                        if place in mine_list_list[j]:
                            safe = False
                        else:
                            unsafe = False

                if unsafe == True:
                    out = False
                    entry_list[place]['background'] = 'red'
                    stringvar_list[place].set('-1')
                if safe == True:
                    out = False
                    entry_list[place]['background'] = 'green'

    # 最小概率判断
    if out == True:
        count_prob_list = []
        other_prob = 0

        for i in range(len(total_count_list)):
            count_prob_list.append(0)

        # 利用等概率原理求出每个未知格子是雷的概率
        total_state_num = 0
        len_other_list = len(other_list)

        for i in range(len(mine_list_list_possible)):
            # 较为复杂的状态数计算
            state_num = 1
            len_mine_list = len(mine_list_list_possible[i])
            if mine_max > mine_remaining:
                mine_max = mine_remaining
            for x in range(mine_max - len(mine_list_list_possible[i])):
                state_num = state_num * (len_other_list - mine_remaining + len_mine_list + x + 1)
                state_num = state_num / (mine_remaining - mine_max + x + 1)
            for j in range(len(total_count_list)):
                if total_count_list[j] in mine_list_list_possible[i]:
                    count_prob_list[j] += state_num
            if len_other_list != 0:
                other_prob += state_num * (mine_remaining - len_mine_list) / len_other_list
            total_state_num += state_num

        count_prob_min = min(count_prob_list)

        if count_prob_min <= other_prob or len_other_list == 0:
            for i in range(len(total_count_list)):
                if count_prob_list[i] == count_prob_min:
                    entry_list[total_count_list[i]]['background'] = 'blue'
                    i_0 = total_count_list[i] // (n + 2) - 1
                    j_0 = total_count_list[i] % (n + 2) - 1
                    print('{}行{}列最不可能是雷，是雷的概率为{}'.format(i_0 + 1, j_0 + 1,
                                                                       count_prob_min / total_state_num))
        else:
            for place in other_list:
                entry_list[place]['background'] = 'blue'
                i_0 = place // (n + 2) - 1
                j_0 = place % (n + 2) - 1
                print('{}行{}列最不可能是雷，是雷的概率为{}'.format(i_0 + 1, j_0 + 1,
                                                                   other_prob / total_state_num))


def reset():
    for i in range((n + 2) * (m + 2)):
        stringvar_list[i].set('0')
        entry_list[i]['background'] = 'white'
        entry_list[i]['foreground'] = 'black'
    for i in range(m):
        for j in range(n):
            stringvar_list[n + 3 + j + (n + 2) * i].set('')


root = tk.Tk()
root.geometry("{}x{}".format(30 * n, 30 * m + 60))
root.title("Minesweeper Solver")
root.resizable(False, False)

for i in range((n + 2) * (m + 2)):
    state_list.append('')
    stringvar_list.append(tk.StringVar())
    entry_list.append(tk.Entry(root, textvariable=stringvar_list[i], width=3))
    stringvar_list.append(tk.StringVar())

for i in range(m):
    for j in range(n):
        entry_list[n + 3 + j + (n + 2) * i].place(x=30 * j, y=30 * i)

for i in range((n + 2) * (m + 2)):
    stringvar_list[i].set('0')
for i in range(m):
    for j in range(n):
        stringvar_list[n + 3 + j + (n + 2) * i].set('')

tk.Button(root, text="Solve", command=cal_prob).place(x=20 * n, y=30 * m + 10)
tk.Button(root, text="Reset", command=reset).place(x=10 * n, y=30 * m + 10)

root.mainloop()






