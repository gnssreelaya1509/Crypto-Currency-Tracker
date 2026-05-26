import flet as ft
import time
from core.engine import GameEngine


def main(page: ft.Page):
    page.title = "Crypto Dash Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B0E14"
    page.padding = 20

    engine = GameEngine()
    game_state = {"last_price": engine.get_crypto_price(), "score": 0, "streak": 0}

    # UI Components
    price_card = ft.Container(
        content=ft.Column([
            ft.Text("BITCOIN PRICE (USD)", color="#848E9C", size=12),
            ft.Text(f"${game_state['last_price']:,}", size=45, weight="bold", color="#F0B90B")
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=30,
        bgcolor="#1E293B",
        border_radius=20,
        border=ft.Border(
            top=ft.BorderSide(1, "#363C4E"),
            bottom=ft.BorderSide(1, "#363C4E"),
            left=ft.BorderSide(1, "#363C4E"),
            right=ft.BorderSide(1, "#363C4E")
        )
    )

    status_text = ft.Text("Predict the next move!", size=16, color="white")
    timer_text = ft.Text("30", size=60, weight="bold", color="#F0B90B")
    score_display = ft.Text("Score: 0 | Streak: 0", size=18)

    # History List
    history_list = ft.ListView(height=100, spacing=5, padding=10)

    btn_up = ft.ElevatedButton("HIGHER ⬆️", style=ft.ButtonStyle(bgcolor="#0ECB81", color="white"),
                               on_click=lambda e: play_round("up"))
    btn_down = ft.ElevatedButton("LOWER ⬇️", style=ft.ButtonStyle(bgcolor="#F6465D", color="white"),
                                 on_click=lambda e: play_round("down"))

    def play_round(choice):
        btn_up.disabled = True
        btn_down.disabled = True
        status_text.value = "Market Locked..."
        page.update()

        async def timer_loop():
            for i in range(30, 0, -1):
                timer_text.value = str(i)
                page.update()
                time.sleep(1)

            new_price = engine.get_crypto_price()
            price_card.content.controls[1].value = f"${new_price:,}"

            # Logic: Compare new price vs OLD reference price
            if (choice == "up" and new_price > game_state['last_price']) or \
                    (choice == "down" and new_price < game_state['last_price']):
                game_state['score'] += 1
                game_state['streak'] += 1
                status_text.value = f"Win! Price reached ${new_price:,}"
            else:
                game_state['streak'] = 0
                status_text.value = f"Lost! Price reached ${new_price:,}"

            # Update History
            history_list.controls.insert(0, ft.Text(f"Last Move: ${new_price:,}", size=12, color="#848E9C"))
            if len(history_list.controls) > 3:
                history_list.controls.pop()

            # Update state memory for next round
            game_state['last_price'] = new_price

            # Reset UI
            score_display.value = f"Score: {game_state['score']} | Streak: {game_state['streak']}"
            btn_up.disabled = False
            btn_down.disabled = False
            timer_text.value = "30"
            page.update()

        page.run_task(timer_loop)

    page.add(
        ft.Column([
            ft.Text("CRYPTO TERMINAL", size=24, weight="bold"),
            price_card,
            score_display,
            timer_text,
            status_text,
            ft.Row([btn_up, btn_down], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Text("PRICE HISTORY", size=12, color="#F0B90B", weight="bold"),
            history_list
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )


ft.app(target=main)