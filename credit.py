#Redudant because of the need of a website demo
# also aint work



# p.init()
# cred_screen = p.display.set_mode((700, 500))
# p.display.set_caption("Two Games in One")
# clock = p.time.Clock()
# running = True
# black = (0, 0, 0)

# while running:
#     for event in p.event.get():
#         if event.type == p.QUIT:
#             running = False
#         if p.key.get_pressed()[p.K_ESCAPE]:
#             running = False
#     cred_screen.fill((150, 150, 150))
#     main = p.font.Font("fonts\\Bokor-Regular.ttf", 50)
#     title = main.render("Credits", True, black)
#     cred_screen.blit(title, (287, 25))

#     norm = p.font.Font("fonts\\Bokor-Regular.ttf", 30)
#     text1 = norm.render("Adrian - Artist(Made All Graphics)", True, black)
#     text2 = norm.render("Aiden - Coder(Created Cards' System)", True, black)
#     text3 = norm.render("Saman - Coder(Created the Enemy System)", True, black)
#     text4 = norm.render("Andrew - Musician(Created Every Sound)", True, black)
#     cred_screen.blit(text1, (170, 130))
#     cred_screen.blit(text2, (140, 185))
#     cred_screen.blit(text4, (120, 235))
#     cred_screen.blit(text3, (116, 285))

#     p.display.flip()
#     clock.tick(60)
# p.quit()