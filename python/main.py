import sqlite3
import os,binascii
import requests,json,time

def send(message,id):
	r = requests.post('http://localhost/exec.php', data = {'message':message , 'id':sender , 'type':'enviar'})
	return(r.text)

def send2(message,id):
	r = requests.post('http://localhost/exec.php', data = {'message':message , 'id':id , 'type':'enviar'})
	return(r.text)
	
def recibir():
	r = requests.post('http://localhost/exec.php', data = {'type':'recibir'})
	return(json.loads(r.text))
	
def audit(text):
	if(text != ""):
		send(text, 3)
	old = recibir()
	told = []
	while(True):
		chec = recibir()
		if(chec != old):
			if(chec["id"] == sender):
				old = recibir()
				told = []
				return(old["message"])
			else:
				try:
					told.index(chec["id"])
				except:
					send2("The chatbot is currenty unavailable. Try again in a while",chec["id"])
					told.append(chec["id"])
		time.sleep(1)
def audit2():
	old = recibir()
	told = []
	while(True):
		chec = recibir()
		if(chec != old):
			old = recibir()
			return(old)
		time.sleep(1)
		
		
accs = sqlite3.connect("accounts.db")
classif = sqlite3.connect("classifications.db")

while(True):
    #Wait and receive message
    men = audit2()
    message = men["message"]
    ide = 345194385
    sender = men["id"]
    nom = men["name"]
    accs.execute("UPDATE clients SET name=? WHERE id=?;", (nom, ide))
	
    xmessage = ""
    for letter in message:
        if letter.isalpha() or letter.isnumeric() or letter == " ":
            xmessage += letter

    #Dissect message in words and a number(if there is)
    sets = xmessage.split()
    words = []
    number = 0
    for i in range(len(sets)):
        if sets[i].isnumeric():
            number = int(sets[i])
        elif sets[i][:-1].isnumeric():
            number = int(sets[i][:-1])
        else:
            words.append(sets[i].lower())

    #Get probability distributions
    probs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    go = 0
    for word in words:
        if word == "friends" or word == "contacts" or word == "people" or word == "accounts":
            go = 1
        try:
            generic = classif.execute("SELECT * FROM pablo WHERE word = ?;", (word, )).fetchone()[1:11]
            for n in range(len(probs)):
                probs[n] += generic[n]
        except:
            pass

    fun = probs.index(max(probs))+1
##    send("Function "+str(fun)+" will be executed.")
	


    #define the different functions

    #READING FUNCTIONS
    if go == 1:
        hehe = accs.execute("SELECT name FROM clients").fetchall()[1:]
        send("List of contacts:", ide)
        for fry in hehe:
            send("-"+fry[0], ide)
        continue
		
    if fun == 1:
        hehe = accs.execute("SELECT name, balance FROM clients where id = ?", (ide, )).fetchone()[0:2]
        send("Hello, "+ hehe[0] +". Your balance is "+ str(hehe[1]) +"€.", ide)
        
    if fun == 2:
        if number == 0:
            number = 3
        name, ISBN = accs.execute("SELECT name, ISBN FROM clients where id = ?", (ide, )).fetchone()[0:2]
        send("Hello, "+name+".  These are your last "+str(number)+" movements:",ide)

        n = 0
        nn = 0
        while(n < number):
            try:
                hehe = accs.execute("SELECT user, amount FROM movements ORDER BY ROWID DESC LIMIT 1 OFFSET ?;", (nn, )).fetchone()[0:2]
            except:
                break
            if accs.execute("SELECT ISBN FROM movements where user = ?", (hehe[0], )).fetchone()[0] == ISBN:
                if hehe[1] > 0:
                    send("+"+str(hehe[1])+"€ from "+str(hehe[0])+".",ide)
                else:
                    send(str(hehe[1])+"€ to "+str(hehe[0])+".",ide)
                n += 1
            nn += 1

    if fun == 3:
        if number == 0:
            number = 3
        name, ISBN = accs.execute("SELECT name, ISBN FROM clients where id = ?", (ide, )).fetchone()[0:2]
        send("Hello, "+name+".  These are your last "+str(number)+" deposits:",ide)

        n = 0
        nn = 0
        while(n < number):
            try:
                hehe = accs.execute("SELECT user, amount FROM movements ORDER BY ROWID DESC LIMIT 1 OFFSET ?;", (nn, )).fetchone()[0:2]
            except:
                break
            if hehe[1] > 0 and accs.execute("SELECT ISBN FROM movements where user = ?", (hehe[0], )).fetchone()[0] == ISBN:
                send("+"+str(hehe[1])+"€ from "+str(hehe[0])+".",ide)
                n += 1
            nn += 1

    if fun == 4:
        if number == 0:
            number = 3
        name, ISBN = accs.execute("SELECT name, ISBN FROM clients where id = ?", (ide, )).fetchone()[0:2]
        send("Hello, "+name+".  These are your last "+str(number)+" debits:",ide)

        n = 0
        nn = 0
        while(n < number):
            try:
                hehe = accs.execute("SELECT user, amount FROM movements ORDER BY ROWID DESC LIMIT 1 OFFSET ?;", (nn, )).fetchone()[0:2]
            except:
                break
            if hehe[1] < 0 and accs.execute("SELECT ISBN FROM movements where user = ?", (hehe[0], )).fetchone()[0] == ISBN:
                send(str(hehe[1])+"€ to "+str(hehe[0])+".",ide)
                n += 1
            nn += 1

    if fun == 5:
        name, ISBN = accs.execute("SELECT name, ISBN FROM clients where id = ?", (ide, )).fetchone()[0:2]
        send("Hello, "+name+". These are your currently active credit cards:",ide)
        n = 1
        while(True):
            try:
                accs.execute("SELECT name, balance FROM cards WHERE ROWID = ?;", (n, )).fetchone()[0]
            except:
                break
            hehe = accs.execute("SELECT ISBN, name, balance FROM cards WHERE ROWID = ?;", (n, )).fetchone()[0:3]
            if hehe[0] == ISBN:
                send(hehe[1]+", with a balance of "+str(hehe[2])+"€.",ide)
            n += 1

    if fun == 6:
        send("You can check our promotions and offers in the link www.coopwork.com!", ide)

    #WRITING FUNCTIONS
    if fun == 7:
        name2 = None
        name, ISBN = accs.execute("SELECT name, ISBN FROM clients where id = ?", (ide, )).fetchone()[0:2]
        ok = 0
        for word in words:
            try:
                word = word[0].upper()+word[1:]
                name2 = accs.execute("SELECT name FROM clients WHERE name = ?", (word,)).fetchone()[0]
                ok = 1
                break
            except:
                pass
        if ok == 0:
            name2 = audit("Who do you want to give money to? ")
            try:
                accs.execute("SELECT name FROM clients WHERE name = ?", (name2,)).fetchone()[0]
            except:
                send("Sorry, I can not understand you.",ide)
                continue
		
        if number == 0:
            number = audit("How much money do you want to send? ")
            if number.isnumeric() and int(number) > 0:
                number = int(number)
            elif number[:-1].isnumeric() and int(number[:-1]) > 0:
                number = int(number[:-1])
            else:
                send("Sorry, I can not understand you.",ide)    
                continue
        send("Hello, "+name+". Do you confirm transferring "+str(number)+"€ to "+name2+"? (Yes or No)",ide)

        resp = audit("")
        if resp == "Yes":
            balance = accs.execute("SELECT balance FROM clients WHERE name=?;", (name,)).fetchone()[0]
            if balance-number < 0:
                send("You don't have enough funds to do that.",ide)
                continue
            accs.execute("UPDATE clients SET balance=? WHERE name=?;", (balance-number, name))
            
            balance2 = accs.execute("SELECT balance FROM clients WHERE name=?;", (name2,)).fetchone()[0]
            accs.execute("UPDATE clients SET balance=? WHERE name=?;", (balance2+number, name2))
            send(str(number)+"€ transferred to "+name2+".", ide)
        if resp == "No":
            send("Thank you for contacting me!", ide)

    if fun == 8:
        name = accs.execute("SELECT name FROM clients where id = ?", (ide, )).fetchone()[0]
        if number == 0:
            for inp in audit("How much money? ").split():
                try:
                    number = int(inp)
                    break
                except:
                    try:
                        number = int(inp[:-1])
                    except:
                        pass
            if number == 0:
                send("Sorry, I can not understand you.",ide)
                continue

        resp = audit(name+", would you like to withdraw "+str(number)+"€ at the nearest ATM? (Yes or No) ")
        if resp == "Yes":
            send(binascii.b2a_hex(os.urandom(3)).decode("utf-8")+" (The debit will be charged when you use the code. It will expire in a 48 hour span)",ide)
        if resp == "No":
            send("Thank you for contacting me!",ide)

    if fun == 9:
        name = accs.execute("SELECT name FROM clients where id = ?", (ide, )).fetchone()[0]
        ss = []
        months = None
        for word in sets:
            if word.isnumeric():
                ss.append(int(word))
            elif word[:-1].isnumeric():
                ss.append(int(word[:-1]))
        if len(ss) > 2:
            send("Sorry, I can not understand you.", ide)
            continue
        try:
            if len(ss) == 0:
                leel = audit("How much money do you want? ")
                if leel.isnumeric():
                    ss.append(int(leel))
                elif leel[:-1].isnumeric():
                    ss.append(int(leel[:-1]))
        except:
            send("Sorry, I can not understand you.", ide)
            continue
        if len(ss) == 1:
            money = int(ss[0])
            months = audit("In how many months you want to divide your payment? ")
            try:
                months.append("lol")
                months = months[0]
            except:
                months = int(months)
                pass
        if len(ss) == 2:
            money = max(ss)
            months = min(ss)

        resp = audit(name+", do you agree getting "+str(money)+"€, paying back "+str(int(1.2*money/months))+"€ each month for "+str(months)+" months? (Yes or No) ")
        if resp == "Yes":
            balance = accs.execute("SELECT balance FROM clients WHERE name=?;", (name,)).fetchone()[0]
            accs.execute("UPDATE clients SET balance=? WHERE name=?;", (balance+money, name))
            send("Credit granted!",ide)
        if resp == "No":
            send("Thank you for contacting me!",ide)

    if fun == 10:
        name = accs.execute("SELECT name FROM clients where id = ?", (ide, )).fetchone()[0]
        if number == 0:
            for inp in audit("How much money? ").split():
                try:
                    number = int(inp)
                    break
                except:
                    try:
                        number = int(inp[:-1])
                    except:
                        pass
            if number == 0:
                send("Sorry, I can not understand you.",ide)
                continue
            
        resp = audit(name+", do you want to transfer "+str(number)+"€ to your phone balance? (Yes or No) ")
        if resp == "Yes":
            balance = accs.execute("SELECT balance FROM clients WHERE name=?;", (name,)).fetchone()[0]
            accs.execute("UPDATE clients SET balance=? WHERE name=?;", (balance-number, name))
            send("Credit granted!", ide)
        if resp == "No":
            send("Thank you for contacting me!" ,ide )

    accs.commit()