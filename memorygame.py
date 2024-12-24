import pygame
import random
import time

# 게임 초기화 설정
pygame.init()

# 화면 설정
SCREEN_WIDTH = 1000  # 화면 너비를 1000으로 변경
SCREEN_HEIGHT = 800  # 화면 높이를 800으로 변경
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('크리스마스 메모리 게임')

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 게임 설정
CARD_WIDTH = 150
CARD_HEIGHT = 150
CARD_MARGIN = 10
ROWS = 4
COLS = 4

# 폰트 설정
FONT = pygame.font.Font('font/notosans.ttf', 36)

# 크리스마스 테마 이미지 리스트 (실제 이미지 파일 경로로 대체해야 함)
CHRISTMAS_IMAGES = [
    'images/santa.png', 'images/reindeer.png', 'images/snowman.png', 'images/tree.png', 
    'images/gift.png', 'images/bell.png', 'images/star.png', 'images/candy.png'
]

class MemoryGame:
    def __init__(self):
        # 카드 이미지 준비
        self.card_images = CHRISTMAS_IMAGES * 2
        random.shuffle(self.card_images)
        
        # 카드 상태 관리
        self.cards = []
        self.revealed_cards = []
        self.matched_cards = []
        
        # 카드 생성
        for row in range(ROWS):
            for col in range(COLS):
                x = col * (CARD_WIDTH + CARD_MARGIN) + 100
                y = row * (CARD_HEIGHT + CARD_MARGIN) + 100
                card_img = self.card_images[row * COLS + col]
                self.cards.append({
                    'rect': pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT),
                    'image': card_img,
                    'revealed': False,
                    'flipping': False,
                    'flip_angle': 0  # 회전 각도
                })
        
        # 게임 상태
        self.attempts = 0
        self.start_time = time.time()
        self.waiting_for_second_card = False  # 두 번째 카드에 대한 대기 상태
        self.second_card_time = 0  # 두 번째 카드 보여주는 시간
        self.waiting_for_flip = False  # 카드 뒤집기 대기 상태

    def draw(self):
        SCREEN.fill(WHITE)
        
        # 카드 그리기
        for card in self.cards[:]:
            if card in self.matched_cards:
                continue  # 맞춘 카드는 그리지 않음
            if card in self.revealed_cards:
                # 카드가 뒤집혔을 때 이미지 로드 및 표시
                img = pygame.image.load(card['image'])
                img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
                SCREEN.blit(img, card['rect'])
            else:
                # 카드 뒷면 그리기 (회전 애니메이션 적용)
                if card['flipping']:
                    # 카드가 회전 중일 때
                    angle = card['flip_angle']
                    rotated_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
                    rotated_surface.fill(RED)  # 카드 뒷면 색
                    rotated_surface.set_colorkey((255, 255, 255))  # 투명색 설정
                    rotated_surface = pygame.transform.rotate(rotated_surface, angle)
                    rotated_rect = rotated_surface.get_rect(center=card['rect'].center)
                    SCREEN.blit(rotated_surface, rotated_rect)
                else:
                    # 회전이 끝난 후 뒷면 그대로 그리기
                    pygame.draw.rect(SCREEN, RED, card['rect'])
        
        # 시도 횟수 표시
        attempts_text = FONT.render(f'시도 횟수: {self.attempts}', True, BLACK)
        SCREEN.blit(attempts_text, (50, 50))
        
        pygame.display.flip()

    def handle_click(self, pos):
        # 첫 번째 카드가 선택되면 바로 뒤집기 시작
        if len(self.revealed_cards) < 2 and not self.waiting_for_flip:
            for card in self.cards:
                if card['rect'].collidepoint(pos) and card not in self.matched_cards and card not in self.revealed_cards:
                    card['flipping'] = True  # 회전 애니메이션 시작
                    self.revealed_cards.append(card)
                    break

        # 두 번째 카드를 선택했을 때
        if len(self.revealed_cards) == 2:
            self.attempts += 1
            self.waiting_for_flip = True  # 카드 뒤집는 동안 다른 카드 클릭 방지
            self.second_card_time = pygame.time.get_ticks()  # 0.5초 시간 기록
            pygame.time.set_timer(pygame.USEREVENT, 500)  # 0.5초 후 타이머 이벤트 시작

    def update_flip(self):
        for card in self.cards:
            if card['flipping']:
                # 회전 각도를 증가시켜 카드가 회전하도록 함
                card['flip_angle'] += 15
                if card['flip_angle'] >= 90:  # 90도 회전 시 뒤집힌 것으로 처리
                    card['flipping'] = False
                    card['revealed'] = True  # 카드가 뒤집혀서 보여짐

    def is_game_over(self):
        return len(self.matched_cards) == ROWS * COLS 

    def show_game_over(self):
        end_time = time.time()
        total_time = int(end_time - self.start_time)
        
       
        SCREEN.fill(WHITE)
        game_over_text = FONT.render('게임 완료!', True, RED)
        time_text = FONT.render(f'총 시간: {total_time}초', True, BLACK)
        attempts_text = FONT.render(f'시도 횟수: {self.attempts}', True, BLACK)
        completion_text = FONT.render('다 맞추셨습니다!', True, GREEN)  # 완료 메시지 추가


        record_text = FONT.render(f'최종 기록된 시간: {total_time}초', True, GREEN)
     
    
        
        SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
        SCREEN.blit(time_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        SCREEN.blit(attempts_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
        SCREEN.blit(completion_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100))  # 완료 메시지 위치
        
        pygame.display.flip()
        pygame.time.wait(3000)

    def remove_matched_cards(self):
        # 맞춘 카드를 바로 삭제
        self.cards = [card for card in self.cards if card not in self.matched_cards]

def main():
    game = MemoryGame()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)
            
            # 2초 후 타이머 이벤트 처리
            if event.type == pygame.USEREVENT:
                # 두 카드가 일치하는지 확인하고 다시 뒤집기
                if len(game.revealed_cards) == 2:
                    if game.revealed_cards[0]['image'] == game.revealed_cards[1]['image']:
                        game.matched_cards.extend(game.revealed_cards)  # 일치하는 카드 추가
                        game.remove_matched_cards()  # 맞춘 카드를 바로 삭제
                    else:
                        game.revealed_cards[0]['revealed'] = False
                        game.revealed_cards[1]['revealed'] = False
                    game.revealed_cards.clear()

                # 타이머 이벤트 종료 후 카드 클릭 가능하도록 상태 변경
                game.waiting_for_flip = False
                pygame.time.set_timer(pygame.USEREVENT, 0)  # 타이머 종료

        game.update_flip()  # 회전 애니메이션 업데이트
        game.draw()
        
        if game.is_game_over():
            game.show_game_over()
            running = False
    
    pygame.quit()

if __name__ == '__main__':
    main()