import random
import time

def print_divider():
    print("\n" + "=" * 50 + "\n")

def get_computer_decision(strategy, comp_score, user_score, turn_score):
    """
    根据选择的策略和当前局势，决定电脑是继续 Roll (返回 True) 还是 Hold (返回 False)
    """
    target_score = 100
    
    # 1. 斩杀线判定：如果当前临时分加上总分已经能赢，直接 Hold 拿满分获胜
    if comp_score + turn_score >= target_score:
        return False

    # 2. 简单策略：稳健保守，只要拿到 15 分就收手
    if strategy == "1":
        return turn_score < 15

    # 3. 中等策略：经典博弈论分界点 Hold at 20
    elif strategy == "2":
        return turn_score < 20

    # 4. 困难策略：Gettysburg 动态博弈最优解 (Optimal)
    elif strategy == "3":
        # 残局阶段：任何一方超过 71 分
        if user_score >= 71 or comp_score >= 71:
            if user_score > comp_score:
                # 电脑落后：必须要追上对方或直达100分，否则不收手
                threshold = min(target_score - comp_score, max(21, user_score - comp_score + 1))
            else:
                # 电脑领先：稳扎稳打防守
                threshold = min(target_score - comp_score, 19)
        else:
            # 常规阶段：根据分差动态调整
            diff = comp_score - user_score
            if diff < -20:    # 大幅落后，开启高风险高回报模式
                threshold = 25
            elif diff > 20:   # 大幅领先，见好就收降低风险
                threshold = 16
            else:             # 均势局
                threshold = 21
                
        return turn_score < threshold

def play_pig_game():
    print("      Welcome to 'The Game of Pig' (人机对战版)      ")
    print("规则：先达到 100 分者获胜。掷出 1 则当回合临时分清零并强制换人。")
    print_divider()

    # 难度选择
    print("请选择电脑 AI 策略难度：")
    print("1. 简单 (保守型 - Hold at 15)")
    print("2. 中等 (经典型 - Hold at 20)")
    print("3. 困难 (动态博弈型 - Optimal)")
    strategy = input("请输入数字 (1/2/3): ").strip()
    if strategy not in ["1", "2", "3"]:
        print("无效输入，默认选择 [2. 中等难度]")
        strategy = "2"

    # 初始化分数
    scores = [0, 0]  # scores[0] 是玩家，scores[1] 是电脑
    player_names = ["玩家 (你)", "电脑 (AI)"]
    current_player = 0 # 0开始代表玩家先手
    target_score = 100

    print_divider()
    print("🎉 游戏正式开始！")

    while max(scores) < target_score:
        print(f"🏆 当前总比分 ->  【{player_names[0]}: {scores[0]}分】 vs 【{player_names[1]}: {scores[1]}分】")
        print(f"👉 当前回合掌控者：【{player_names[current_player]}】")
        
        turn_score = 0
        turn_active = True

        while turn_active:
            print(f"   💡 当前回合累积临时分: {turn_score}")
            
            # --- 玩家 1 的操作分支 ---
            if current_player == 0:
                choice = input("   输入 'r' 掷骰子 (Roll)，输入 'h' 停手存分 (Hold): ").strip().lower()
                
                if choice == 'r':
                    roll = random.randint(1, 6)
                    print(f"   🎲 你摇出了: {roll}")
                    
                    if roll == 1:
                        print("   💥 哎呀！踩到 1 了！本回合临时得分全部清零 😭")
                        turn_score = 0
                        turn_active = False
                    else:
                        turn_score += roll
                        if scores[0] + turn_score >= target_score:
                            print("   检测到你的分数已经足够获胜，自动为您 Hold 存分！")
                            turn_active = False
                elif choice == 'h':
                    turn_active = False
                else:
                    print("   ⚠️ 无效输入，请输入 'r' 或 'h'。")

            # --- 电脑 (AI) 的操作分支 ---
            else:
                time.sleep(1) # 增加 1 秒延迟，模拟电脑思考过程，让控制台信息不会闪得太快
                # 调用我们在上面写的 AI 决策函数
                keep_rolling = get_computer_decision(strategy, scores[1], scores[0], turn_score)
                
                if keep_rolling:
                    roll = random.randint(1, 6)
                    print(f"   🎲 电脑决定继续 Roll，摇出了: {roll}")
                    
                    if roll == 1:
                        print("   💥 哈哈！电脑也摇到了 1！本回合它的临时分同样清零 🤪")
                        turn_score = 0
                        turn_active = False
                    else:
                        turn_score += roll
                else:
                    print(f"   🤖 电脑经过精确计算，决定选择 Hold 见好就收。")
                    turn_active = False

        # --- 回合结束，结算分数 ---
        scores[current_player] += turn_score
        print(f"\n✨ {player_names[current_player]} 在本轮最终斩获: {turn_score} 分！")
        
        # 胜负检查
        if scores[current_player] >= target_score:
            print_divider()
            if current_player == 0:
                print(f"🏆🎉🏆 恭喜你！！你成功击败了电脑，赢得了最终胜利！！！ 🏆🎉🏆")
            else:
                print(f"🤖 电脑抢先达到了 {scores[1]} 分！胜败乃兵家常事，少侠请重新来过。")
            break

        # 切换到下一个玩家 (0 变 1，1 变 0)
        current_player = 1 - current_player
        print_divider()

if __name__ == "__main__":
    play_pig_game()