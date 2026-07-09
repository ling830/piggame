import random
import time
import sys

# 引入 Windows 专属的键盘即时响应库
try:
    import msvcrt
except ImportError:
    print("提示：该免回车版本需要 Windows 系统环境。")
    sys.exit()

def print_divider():
    print("\n" + "=" * 50 + "\n")

def get_char_immediate():
    """ 核心练习函数：无需回车，直接捕获键盘按下的单个字符 """
    # msvcrt.getch() 会抓取原生的字节，我们需要用 decode 把它转成普通的字符串字母
    char = msvcrt.getch().decode('utf-8', errors='ignore')
    return char.lower()

def get_computer_decision(strategy, comp_score, user_score, turn_score):
    """ AI 动态阈值博弈算法 """
    target_score = 100
    if comp_score + turn_score >= target_score:
        return False

    if strategy == "1":
        return turn_score < 15
    elif strategy == "2":
        return turn_score < 20
    elif strategy == "3":
        let_user_lead = user_score >= 71 or comp_score >= 71
        if let_user_lead:
            if user_score > comp_score:
                threshold = min(target_score - comp_score, max(21, user_score - comp_score + 1))
            else:
                threshold = min(target_score - comp_score, 19)
        else:
            diff = comp_score - user_score
            if diff < -20: threshold = 25
            elif diff > 20: threshold = 16
            else: threshold = 21
        return turn_score < threshold

def play_pig_game():
    print("      Welcome to 'The Game of Pig' (免回车人机版)      ")
    print("规则：先到 100 分获胜。直接敲击对应按键，无需按回车确认！")
    print_divider()

    # 1. 难度选择（免回车）
    print("请直接按下键盘上的数字 [1]、[2] 或 [3] 选择电脑难度：")
    print("1. 简单 (Hold at 15)")
    print("2. 中等 (Hold at 20)")
    print("3. 困难 (Optimal 动态最优解)")
    
    while True:
        strategy = get_char_immediate()
        if strategy in ["1", "2", "3"]:
            break
    
    strategy_names = {"1": "简单", "2": "中等", "3": "困难"}
    print(f"➔ 已选择难度：【{strategy_names[strategy]}】")
    
    # 初始化分数
    scores = [0, 0] 
    player_names = ["玩家 (你)", "电脑 (AI)"]
    current_player = 0 
    target_score = 100

    print_divider()
    print("🎉 游戏开始！")

    while max(scores) < target_score:
        print(f"🏆 总比分 -> 【{player_names[0]}: {scores[0]}分】 vs 【{player_names[1]}: {scores[1]}分】")
        print(f"👉 当前回合：【{player_names[current_player]}】")
        
        turn_score = 0
        turn_active = True

        while turn_active:
            print(f"   💡 当前回合临时分: {turn_score}")
            
            # --- 玩家 1 的操作分支（免回车） ---
            if current_player == 0:
                print("   [直接按 F 键]: 掷骰子(Roll)  |  [直接按 G 键]: 停手存分(Hold) ", end="", flush=True)
                
                # 阻塞等待玩家按下 F 或 G
                while True:
                    key = get_char_immediate()
                    if key in ['f', 'g']:
                        break
                print() # 换行，保持控制台整洁
                
                if key == 'f':
                    roll = random.randint(1, 6)
                    print(f"   🎲 你摇出了: {roll}")
                    
                    if roll == 1:
                        print("   💥 踩到 1 了！本回合临时分清零！")
                        turn_score = 0
                        turn_active = False
                    else:
                        turn_score += roll
                        if scores[0] + turn_score >= target_score:
                            print("   分数已足够获胜，自动为您存分！")
                            turn_active = False
                            
                elif key == 'g':
                    turn_active = False

            # --- 电脑 (AI) 的操作分支 ---
            else:
                time.sleep(0.8) # 模拟思考延迟
                keep_rolling = get_computer_decision(strategy, scores[1], scores[0], turn_score)
                
                if keep_rolling:
                    roll = random.randint(1, 6)
                    print(f"   🎲 电脑决定继续 Roll，摇出了: {roll}")
                    if roll == 1:
                        print("   💥 电脑摇到了 1！本回合它的临时分清零。")
                        turn_score = 0
                        turn_active = False
                    else:
                        turn_score += roll
                else:
                    print(f"   🤖 电脑选择 Hold 存分。")
                    turn_active = False

        # --- 回合结算 ---
        scores[current_player] += turn_score
        print(f"\n✨ {player_names[current_player]} 本轮最终获得: {turn_score} 分！")
        
        if scores[current_player] >= target_score:
            print_divider()
            if current_player == 0:
                print(f"🏆🎉🏆 恭喜你！！你成功击败了电脑，赢得了最终胜利！！！")
            else:
                print(f"🤖 电脑抢先达到了 {scores[1]} 分！游戏结束。")
            break

        current_player = 1 - current_player
        print_divider()

if __name__ == "__main__":
    try:
        play_pig_game()
    except KeyboardInterrupt:
        print("\n👋 游戏已安全退出。")