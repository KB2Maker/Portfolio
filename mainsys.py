import pygame as pg
import random

# PlayerCharacterクラスの定義 [ここから]

class PlayerCharacter:

    # コンストラクタ
    def __init__(self, init_pos, img_path):
        self.pos = pg.Vector2(init_pos)
        self.size = pg.Vector2(48, 64)
        self.dir = 2
        img_raw = pg.image.load(img_path)
        self.__img_arr = []
        for i in range(4):
            self.__img_arr.append([])
            for j in range(3):
                p = pg.Vector2(24 * j, 32 * i)
                tmp = img_raw.subsurface(pg.Rect(p, (24, 32)))
                tmp = pg.transform.scale(tmp, self.size)
                self.__img_arr[i].append(tmp)
            self.__img_arr[i].append(self.__img_arr[i][1])

    def turn_to(self, dir):
        self.dir = dir

    def move_to(self, vec):
        self.pos += vec

    def get_dp(self):
        return self.pos * 48 - pg.Vector2(0, 24)

    def get_img(self, frame):
        return self.__img_arr[self.dir][frame // 6 % 4]

# PlayerCharacterクラスの定義 [ここまで]

def main():

    # 初期化処理
    chip_s = 48  # マップチップの基本サイズ
    map_s = pg.Vector2(16, 9)  # マップの横・縦の配置数 
    # 時間制限システム分の初期化処理
    current_time = 1800  # 制限時間（フレーム）
    display_time = 60
    # コインの初期位置処理
    score = 0
    coin_pos = (random.randint(1, 14), random.randint(1, 7))  # 初期のコインの位置
    coin_image = pg.image.load('./data/img/point.png')

    pg.init()
    pg.display.set_caption('博麗霊夢はお金集めに夢中のようです')
    disp_w = int(chip_s * map_s.x)
    disp_h = int(chip_s * map_s.y)
    screen = pg.display.set_mode((disp_w, disp_h))
    clock = pg.time.Clock()
    font = pg.font.Font(None, 15)
    frame = 0
    exit_flag = False
    exit_code = '000'

    # グリッド設定
    grid_c = '#bbbbbb'

    # 自キャラ移動関連
    cmd_move = -1  # 移動コマンドの管理変数
    m_vec = [
        pg.Vector2(0, -1),
        pg.Vector2(1, 0),
        pg.Vector2(0, 1),
        pg.Vector2(-1, 0)
    ]  # 移動コマンドに対応したXYの移動量

    # 自キャラの生成・初期化
    reimu = PlayerCharacter((2, 3), './data/img/reimu.png')

    # ゲームループ
    while not exit_flag:

        # システムイベントの検出
        cmd_move = -1
        for event in pg.event.get():
            if event.type == pg.QUIT:  # ウィンドウ[X]の押下
                exit_flag = True
                exit_code = '001'
            # 移動操作の「キー入力」の受け取り処理
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    cmd_move = 0
                elif event.key == pg.K_RIGHT:
                    cmd_move = 1
                elif event.key == pg.K_DOWN:
                    cmd_move = 2
                elif event.key == pg.K_LEFT:
                    cmd_move = 3

        # 背景描画
        screen.fill(pg.Color('WHITE'))

        # グリッド
        for x in range(0, disp_w, chip_s):  # 縦線
            pg.draw.line(screen, grid_c, (x, 0), (x, disp_h))
        for y in range(0, disp_h, chip_s):  # 横線
            pg.draw.line(screen, grid_c, (0, y), (disp_w, y))

        # 移動コマンドの処理
        if cmd_move != -1:
            reimu.turn_to(cmd_move)
            af_pos = reimu.pos + m_vec[cmd_move]  # 移動(仮)した座標
            if (0 <= af_pos.x <= map_s.x - 1) and (0 <= af_pos.y <= map_s.y - 1):
                reimu.move_to(m_vec[cmd_move])  # 画面範囲内なら実際に移動

        # 自キャラの描画
        screen.blit(reimu.get_img(frame), reimu.get_dp())

        # フレームカウンタの描画
        frame += 1
        frm_str = f'{frame:05}'
        screen.blit(font.render(frm_str, True, 'BLACK'), (10, 10))
        screen.blit(font.render(f'{reimu.pos}', True, 'BLACK'), (10, 20))
        # コイン取得時の処理
        if reimu.pos == pg.Vector2(coin_pos):
            score += 1  # コインを取得すると得点が追加
            coin_pos = (random.randint(1, 14), random.randint(1, 7))  # 新しいコインをランダムに生成
        score_str = f'{score:03}'
        screen.blit(font.render(score_str, True, 'BLACK'), (700, 30))
        # 表示上の時間の管理
        if frame % 30 == 0:
            display_time -= 1
        dis_str = f'{display_time:02}'
        screen.blit(font.render(dis_str, True, 'BLACK'), (30, 30))
        # 時間切れ処理
        if current_time == frame:
            exit_flag = True  # 時間切れでゲーム終了
            exit_code = '002'
        
        # 新しいコインを描画
        screen.blit(coin_image, (coin_pos[0] * chip_s, coin_pos[1] * chip_s))

        # 画面の更新と同期
        pg.display.update()
        clock.tick(30)

    # ゲームループ [ここまで]
    pg.quit()
    return exit_code

if __name__ == "__main__":
    code = main()
    print(f'プログラムを「コード{code}」で終了しました。')