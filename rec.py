from graphics import *

def item_n_price(win, i, items, prices):
    z = 50 * i
    center = Point(50,50+z)
    label = Text(center, "Item >>")
    label.draw(win)
    input = Entry(Point(170,55+z), 20)
    input.setText("item")
    input.draw(win)
    items.append(input)
    center = Point(350,50+z)
    label = Text(center, "Price >>")
    label.draw(win)
    input = Entry(Point(420,55+z), 6)
    input.setText("0.00")
    input.draw(win)
    prices.append(input)
    
def main():
    win = GraphWin("WalMart Receipt", 600, 900)
    #Title
    center = Point(300,20)
    label = Text(center, "WalMart Receipt Maker")
    label.draw(win)
    label.setSize(20)
    items = []
    prices = []
    
    for i in range(15):
        item_n_price(win, i, items, prices)
    #print receipt button
    rect5 = Rectangle(Point(240,800), Point(360,850))
    rect5.draw(win)
    center5 = Point(300,825)
    button = Text(center5, "Print Receipt")
    button.draw(win)
    button.setSize(10)
    button.setFill('Orange')
    win.getMouse()
    
    win2 = GraphWin("WalMart Receipt", 600, 900)
    #Title 2
    center = Point(300,20)
    label22 = Text(center, "WalMart Receipt")
    label22.draw(win2)
    label22.setSize(20)
    
    output = Text(Point(170,55), "")
    x = eval(prices[1].getText())
    output.setText(x)
    output.draw(win2)
    
    win2.getMouse()
    
    
    
main()
