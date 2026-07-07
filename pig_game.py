import random
import sys

# ========================
# 🐷 猪游戏 (Pig Game) - Python版
# 无需按回车，直接按键响应！
# ========================

def getch():
    """读取单个按键（无需按回车）"""
    try:
        import msvcrt
        return msvcrt.getch().decode('utf-8').lower()
    except ImportError:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def roll_dice():
    """掷骰子，返回1-6的随机数"""
    return random.randint(1, 6)

def show_dice_face(number):
    """用字符画显示骰子"""
    faces = {
        1: """
┌─────────┐
│         │
│    ●    │
│         │
└─────────┘""",
        2: """
┌─────────┐
│  ●      │
│         │
│      ●  │
└─────────┘""",
        3: """
┌─────────┐
│  ●      │
│    ●    │
│      ●  │
└─────────┘""",
        4: """
┌─────────┐
│  ●   ●  │
│         │
│  ●   ●  │
└─────────┘""",
        5: """
┌─────────┐
│  ●   ●  │
│    ●    │
│  ●   ●  │
└─────────┘""",
        6: """
┌─────────┐
│  ●   ●  │
│  ●   ●  │
│  ●   ●  │
└─────────┘"""
    }
    return faces[number]

def print_status(p1_total, p2_total, p1_turn, p2_turn, current_player):
    """打印当前游戏状态"""
    print("\n" + "=" * 50)
    print("           🐷 猪游戏 对战版 🐷")
    print("=" * 50)

    p1_marker = "▶" if current_player == 1 else " "
    print(f"\n  {p1_marker} 玩家1 🔴")
    print(f"     总分: {p1_total}  |  本回合: {p1_turn}")

    p2_marker = "▶" if current_player == 2 else " "
    print(f"\n  {p2_marker} 玩家2 🔵")
    print(f"     总分: {p2_total}  |  本回合: {p2_turn}")

    print("\n" + "-" * 50)

def print_controls(current_player):
    """显示操作提示"""
    if current_player == 1:
        print("\n  玩家1: [F]掷骰  [G]储存  [U]重新开始")
    else:
        print("\n  玩家2: [J]掷骰  [K]储存  [U]重新开始")

def main():
    """主游戏循环"""

    p1_total = 0
    p2_total = 0
    p1_turn = 0
    p2_turn = 0
    current_player = 1
    WIN_SCORE = 100

    print("\n" + "🎉" * 25)
    print("\n         欢迎来到 🐷 猪游戏！")
    print("\n  规则:")
    print("  • 掷骰子，点数累加到【本回合分数】")
    print("  • 掷到 1 → 🐷 猪！本回合分数清零，换对手")
    print("  • 储存 → 本回合分数加入【总分】（永久安全）")
    print("  • 先达到 100 分者获胜！")
    print("\n  💡 提示：直接按 F/J/G/K/U 即可，无需按回车！")
    print("\n" + "🎉" * 25)

    while True:
        print_status(p1_total, p2_total, p1_turn, p2_turn, current_player)
        print_controls(current_player)

        print("\n  请按键...", end="", flush=True)
        command = getch()
        print(command)

        # ========== 玩家1操作 ==========
        if current_player == 1:
            if command == "f":
                dice = roll_dice()
                print(f"\n  🎲 玩家1掷出了: {dice}")
                print(show_dice_face(dice))

                if dice == 1:
                    print("  \n  🐷🐷🐷 猪！本回合分数清零！🐷🐷🐷")
                    print(f"  玩家1本回合的 {p1_turn} 分丢失了...")
                    print(f"  但已储存的 {p1_total} 分是安全的！")
                    p1_turn = 0
                    current_player = 2
                else:
                    p1_turn += dice
                    print(f"  本回合累计: {p1_turn} 分")

            elif command == "g":
                if p1_turn == 0:
                    print("\n  ⚠️ 本回合还没有分数，无法储存！")
                    continue
                p1_total += p1_turn
                print(f"\n  ✅ 玩家1储存了 {p1_turn} 分！")
                print(f"  玩家1总分: {p1_total}（已安全储存）")
                p1_turn = 0

                if p1_total >= WIN_SCORE:
                    print("\n" + "🏆" * 20)
                    print(f"\n  🎉🎉🎉 玩家1 获胜！总分: {p1_total} 🎉🎉🎉")
                    print("\n" + "🏆" * 20)
                    print("\n  按任意键继续...")
                    getch()
                    continue

                current_player = 2

            elif command == "u":
                print("\n  🔄 游戏重新开始！")
                p1_total = p2_total = 0
                p1_turn = p2_turn = 0
                current_player = 1

            else:
                print(f"\n  ❌ 无效按键 '{command}'！玩家1请按 F(掷骰) 或 G(储存)")

        # ========== 玩家2操作 ==========
        elif current_player == 2:
            if command == "j":
                dice = roll_dice()
                print(f"\n  🎲 玩家2掷出了: {dice}")
                print(show_dice_face(dice))

                if dice == 1:
                    print("  \n  🐷🐷🐷 猪！本回合分数清零！🐷🐷🐷")
                    print(f"  玩家2本回合的 {p2_turn} 分丢失了...")
                    print(f"  但已储存的 {p2_total} 分是安全的！")
                    p2_turn = 0
                    current_player = 1
                else:
                    p2_turn += dice
                    print(f"  本回合累计: {p2_turn} 分")

            elif command == "k":
                if p2_turn == 0:
                    print("\n  ⚠️ 本回合还没有分数，无法储存！")
                    continue
                p2_total += p2_turn
                print(f"\n  ✅ 玩家2储存了 {p2_turn} 分！")
                print(f"  玩家2总分: {p2_total}（已安全储存）")
                p2_turn = 0

                if p2_total >= WIN_SCORE:
                    print("\n" + "🏆" * 20)
                    print(f"\n  🎉🎉🎉 玩家2 获胜！总分: {p2_total} 🎉🎉🎉")
                    print("\n" + "🏆" * 20)
                    print("\n  按任意键继续...")
                    getch()
                    continue

                current_player = 1

            elif command == "u":
                print("\n  🔄 游戏重新开始！")
                p1_total = p2_total = 0
                p1_turn = p2_turn = 0
                current_player = 1

            else:
                print(f"\n  ❌ 无效按键 '{command}'！玩家2请按 J(掷骰) 或 K(储存)")

if __name__ == "__main__":
    main()
