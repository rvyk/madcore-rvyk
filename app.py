import re
from flask import Flask, redirect, render_template, request, url_for, jsonify, flash
from flask_mysqldb import MySQL, MySQLdb
from handlers import errors
import time
from mcrcon import MCRcon
import datetime
app = Flask(__name__)
app.secret_key = "!d\_U1<;+*vR@S;pMN0u"
app.register_blueprint(errors)
app.config['MYSQL_HOST'] = '34.116.255.40'
app.config['MYSQL_USER'] = 'rvyk'
app.config['MYSQL_PASSWORD'] = 'skala234'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
mcr = MCRcon("34.116.255.40", "skala234")
@app.route('/'  , methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('user', usr=user))
    else:
        return render_template('strona-glowna.html')

@app.route('/voucher', methods=['POST', 'GET'])
def voucher():
    if request.method == 'POST' and "nm" in request.form:
        user = request.form['nm']
        return redirect(url_for('user', usr=user))
    if request.method == 'POST' and 'username' and 'vouchercode' in request.form:
        username = request.form['username']
        vouchercode = request.form['vouchercode']
        print('username', username)
        print('voucher code', vouchercode)
        cur = mysql.connection.cursor()
        cur.execute("USE voucher")
        cur.execute(f"SELECT usluga FROM vouchers WHERE voucher_code='{vouchercode}'")
        voucherCur = cur.fetchone()
        numrows = int(cur.rowcount)
        if numrows == 0:
            flash("Ten voucher nie istnieje", "info")
            cur.close()
        else:
            try:
                usluga = voucherCur.get("usluga")
                mcr.connect()
                mcr.command(f"lp user {username} parent set {usluga}")
                mcr.disconnect()
                cur.execute(f"DELETE FROM vouchers WHERE voucher_code='{vouchercode}'")
                mysql.connection.commit()
                cur.close()
                flash(f"Voucher został zrealizowany na nick: {username}", "info")
            except:
                flash(f"Serwer jest wyłączony", "info")
                mysql.connection.commit()
                cur.close()

        return redirect(url_for('voucher'))
    return render_template('voucher.html')

@app.route('/topki', methods=['GET', 'POST'])
def topki():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('user', usr=user))
    try:
        cur = mysql.connection.cursor()
        cur.execute("USE kills")
        cur.execute(f"SELECT * FROM `pvpstats` order by `kills` desc limit 10")
        topki = cur.fetchall()
        cur.execute(f"SELECT * FROM `pvpstats` order by `deaths` desc limit 10")
        topki3 = cur.fetchall()
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(e)
        return render_template('topki.html')
        
    return render_template('topki.html', topki=topki, topki3=topki3)

@app.route("/ajaxpost",methods=["POST","GET"])
def ajaxpost():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)    
    if request.method == 'POST':
        queryString = request.form['queryString']
        cur.execute('USE jpremium')
        query = "SELECT * from user_profiles WHERE lastNickname LIKE '{}%' LIMIT 10".format(queryString)
        cur.execute(query)
        players = cur.fetchall()
    return jsonify({'htmlresponse': render_template('response.html', players=players)})

@app.route('/regulamin')
def regulamin():
    return render_template('regulamin.html')
@app.route('/profil/<usr>', methods=['GET', 'POST'])
def user(usr):
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('user', usr=user))
    try:
        cur = mysql.connection.cursor()
        cur.execute("USE jpremium")
        cur.execute(f"SELECT lastNickname,lastSeen,firstSeen,premiumId FROM `user_profiles` WHERE lastNickname='{usr}'")
        jpremium = cur.fetchall()
        numrows = int(cur.rowcount)
        cur.execute(f"SELECT premiumId FROM `user_profiles` WHERE lastNickname='{usr}'")
        premiumid = cur.fetchone()
        premiumid = premiumid.get('premiumId')
        if premiumid != None:
            premiumaccount = True
        if numrows == 0:
            print("Nic nie znaleziono")
            mysql.connection.commit()
            cur.close()
            return render_template('wyszukaj.html', usr=usr, numrows=numrows)
        cur.execute("USE luckperms")
        cur.execute(f"SELECT uuid FROM `luckperms_players` WHERE username='{usr}'")
        uuid = cur.fetchone()
        uuid = uuid.get("uuid")
        if uuid == None:
            uuid = "Nie pobrano"
        cur.execute(f"SELECT primary_group FROM `luckperms_players` WHERE username='{usr}'")
        ranga = cur.fetchone()
        ranga = ranga.get("primary_group")
        if ranga == None:
            ranga = "Nie pobrano"
        elif ranga == 'default':
            ranga = "Gracz"
#playtime
        cur = mysql.connection.cursor()
        cur.execute("USE playtime")
        cur.execute(f"SELECT Seconds FROM `playtimeplus` WHERE Name='{usr}'")
        sekundy = cur.fetchone()
        sekundy = sekundy.get('Seconds')
        print(sekundy)
        if sekundy != None:
            play_time = time.strftime('%H:%M:%S', time.gmtime(sekundy))
        else:
            play_time = "Nie pobrano"
#skiny
        cur.execute("USE skiny")
        cur.execute(f"SELECT Skin FROM `Players` WHERE Nick='{usr}'")
        skiny = cur.fetchone()
        try:
            skiny = skiny.get("Skin")
        except Exception:
            if premiumaccount == True:
                skiny = usr
            else:
                skiny = "None"
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(e)
        return render_template('500.html')
        
    return render_template('wyszukaj.html', skiny=skiny, numrows=numrows, usr=usr, jpremium=jpremium, ranga=ranga, uuid=uuid, play_time=play_time)
@app.route('/profil/statystyki/<usr>', methods=['GET', 'POST'])
def statystykipage(usr):
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('user', usr=user))
    try: 
        cur = mysql.connection.cursor()
        cur.execute("USE jpremium")
        cur.execute(f"SELECT * FROM `user_profiles` WHERE lastNickname='{usr}'")
        jpremium = cur.fetchall()
        numrows = int(cur.rowcount)
        cur.execute(f"SELECT premiumId FROM `user_profiles` WHERE lastNickname='{usr}'")
        premiumid = cur.fetchone()
        premiumid = premiumid.get('premiumId')
        if premiumid != None:
            premiumaccount = True
        if numrows == 0:
            print("Nic nie znaleziono")
            mysql.connection.commit()
            cur.close()
            return render_template('statystyki.html', usr=usr, numrows=numrows)
#GET SKIN
        cur.execute("USE skiny")
        cur.execute(f"SELECT Skin FROM `Players` WHERE Nick='{usr}'")
        skiny = cur.fetchone()
        try:
            skiny = skiny.get("Skin")
        except Exception:
            if premiumaccount == True:
                skiny = usr
            else:
                skiny = "None"
#GET UUID
        cur.execute("USE statystyki")
        cur.execute(f"SELECT uuid FROM `statz_players` WHERE playerName='{usr}'")
        uuid = cur.fetchone()
        uuidvalid = uuid.get("uuid")
#GET BLOCK PLACE
        cur.execute(f"SELECT SUM(value) FROM statz_blocks_placed WHERE uuid='{uuidvalid}'")
        block_place = cur.fetchone()
        block_placevalid = block_place.get("SUM(value)")
        if block_placevalid == None:
            block_placevalid = "Brak danych"
#GET BLOCK BREAK
        cur.execute(f"SELECT SUM(value) FROM statz_blocks_broken WHERE uuid='{uuidvalid}'")
        block_break = cur.fetchone()
        block_breakvalid = block_break.get("SUM(value)")
        if block_breakvalid == None:
            block_breakvalid = "Brak danych"
#MOB KILL
        cur.execute(f"SELECT SUM(value) FROM statz_kills_mobs WHERE uuid='{uuidvalid}'")
        mob_kill = cur.fetchone()
        mob_killvalid = mob_kill.get("SUM(value)")
        if mob_killvalid == None:
            mob_killvalid = "Brak danych"
#DAMAGE TAKEN
        cur.execute(f"SELECT SUM(value) FROM statz_damage_taken WHERE uuid='{uuidvalid}'")
        damage_taken = cur.fetchone()
        damage_takenvalid = damage_taken.get("SUM(value)")
        if damage_takenvalid == None:
            damage_takenvalid = "Brak danych"
#VILLAGER TRADES
        cur.execute(f"SELECT SUM(value) FROM statz_villager_trades WHERE uuid='{uuidvalid}'")
        villager_trades = cur.fetchone()
        villager_tradesvalid = villager_trades.get("SUM(value)")
        if villager_tradesvalid == None:
            villager_tradesvalid = "Brak danych"
#PLAYER KILLS
        cur.execute(f"SELECT SUM(value) FROM statz_kills_players WHERE uuid='{uuidvalid}'")
        kills_players = cur.fetchone()
        kills_playersvalid = kills_players.get("SUM(value)")
        if kills_playersvalid == None:
            kills_playersvalid = "Brak danych"
#TOOLS BROKEN
        cur.execute(f"SELECT SUM(value) FROM statz_tools_broken WHERE uuid='{uuidvalid}'")
        tools_broken = cur.fetchone()
        tools_brokenvalid = tools_broken.get("SUM(value)")
        if tools_brokenvalid == None:
            tools_brokenvalid = "Brak danych"
#ARROWS SHOT
        cur.execute(f"SELECT SUM(value) FROM statz_arrows_shot WHERE uuid='{uuidvalid}'")
        arrows_shot = cur.fetchone()
        arrows_shotvalid = arrows_shot.get("SUM(value)")
        if arrows_shotvalid == None:
            arrows_shotvalid = "Brak danych"
#BUCKETS FILLED
        cur.execute(f"SELECT SUM(value) FROM statz_buckets_filled WHERE uuid='{uuidvalid}'")
        buckets_filled = cur.fetchone()
        buckets_filledvalid = buckets_filled.get("SUM(value)")
        if buckets_filledvalid == None:
            buckets_filledvalid = "Brak danych"
#BUCKETS EMPTIED
        cur.execute(f"SELECT SUM(value) FROM statz_buckets_emptied WHERE uuid='{uuidvalid}'")
        buckets_emptied = cur.fetchone()
        buckets_emptiedvalid = buckets_emptied.get("SUM(value)")
        if buckets_emptiedvalid == None:
            buckets_emptiedvalid = "Brak danych"
#COMMANDS PERFORMED
        cur.execute(f"SELECT SUM(value) FROM statz_commands_performed WHERE uuid='{uuidvalid}'")
        commands_performed = cur.fetchone()
        commands_performedvalid = commands_performed.get("SUM(value)")
        if commands_performedvalid == None:
            commands_performedvalid = "Brak danych"
#ITEMS CRAFTED
        cur.execute(f"SELECT SUM(value) FROM statz_items_crafted WHERE uuid='{uuidvalid}'")
        items_crafted = cur.fetchone()
        items_craftedvalid = items_crafted.get("SUM(value)")
        if items_craftedvalid == None:
            items_craftedvalid = "Brak danych"
#DEATHS
        cur.execute(f"SELECT SUM(value) FROM statz_deaths WHERE uuid='{uuidvalid}'")
        deaths = cur.fetchone()
        deathsvalid = deaths.get("SUM(value)")
        if deathsvalid == None:
            deathsvalid = "Brak danych"
#FOOD EATEN
        cur.execute(f"SELECT SUM(value) FROM statz_food_eaten WHERE uuid='{uuidvalid}'")
        food_eaten = cur.fetchone()
        food_eatenvalid = food_eaten.get("SUM(value)")
        if food_eatenvalid == None:
            food_eatenvalid = "Brak danych"
#ITEMS DROPPED
        cur.execute(f"SELECT SUM(value) FROM statz_items_dropped WHERE uuid='{uuidvalid}'")
        items_dropped = cur.fetchone()
        items_droppedvalid = items_dropped.get("SUM(value)")
        if items_droppedvalid == None:
            items_droppedvalid = "Brak danych"
#ITEMS PICKED UP
        cur.execute(f"SELECT SUM(value) FROM statz_items_picked_up WHERE uuid='{uuidvalid}'")
        items_picked_up = cur.fetchone()
        items_picked_upvalid = items_picked_up.get("SUM(value)")
        if items_picked_upvalid == None:
            items_picked_upvalid = "Brak danych"
#DISTANCE TRAVELLED
        cur.execute(f"SELECT SUM(value) FROM statz_distance_travelled WHERE uuid='{uuidvalid}'")
        distance_travelled = cur.fetchone()
        distance_travelleddecimal = distance_travelled.get("SUM(value)")
        distance_travelledvalid = str(round(distance_travelleddecimal, 2))
        if distance_travelledvalid == None:
            distance_travelledvalid = "Brak danych"
#EGGS THROWN
        cur.execute(f"SELECT SUM(value) FROM statz_eggs_thrown WHERE uuid='{uuidvalid}'")
        eggs_thrown = cur.fetchone()
        eggs_thrownvalid = eggs_thrown.get("SUM(value)")
        if eggs_thrownvalid == None:
            eggs_thrownvalid = "Brak danych"
#ENTERED BEDS
        cur.execute(f"SELECT SUM(value) FROM statz_entered_beds WHERE uuid='{uuidvalid}'")
        entered_beds = cur.fetchone()
        entered_bedsvalid = entered_beds.get("SUM(value)")
        if entered_bedsvalid == None:
            entered_bedsvalid = "Brak danych"
#JOINS
        cur.execute(f"SELECT SUM(value) FROM statz_joins WHERE uuid='{uuidvalid}'")
        joins = cur.fetchone()
        joinsvalid = joins.get("SUM(value)")
        if joinsvalid == None:
            joinsvalid = "0"
#XP GAINED
        cur.execute(f"SELECT SUM(value) FROM statz_xp_gained WHERE uuid='{uuidvalid}'")
        xp_gained = cur.fetchone()
        xp_gainedvalid = xp_gained.get("SUM(value)")
        if xp_gainedvalid == None:
            xp_gainedvalid = "0"
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(e)
        return render_template('500.html')
        
    return render_template('statystyki.html', numrows=numrows,
      usr=usr, jpremium=jpremium, block_placevalid=block_placevalid,
      block_breakvalid=block_breakvalid, mob_killvalid=mob_killvalid,
      damage_takenvalid=damage_takenvalid, villager_tradesvalid=villager_tradesvalid,
      kills_playersvalid=kills_playersvalid, tools_brokenvalid=tools_brokenvalid,
      arrows_shotvalid=arrows_shotvalid, buckets_filledvalid=buckets_filledvalid,
      buckets_emptiedvalid=buckets_emptiedvalid, commands_performedvalid=commands_performedvalid,
      items_craftedvalid=items_craftedvalid, deathsvalid=deathsvalid, food_eatenvalid=food_eatenvalid,
      items_droppedvalid=items_droppedvalid, items_picked_upvalid=items_picked_upvalid,
      distance_travelledvalid=distance_travelledvalid, eggs_thrownvalid=eggs_thrownvalid,
      entered_bedsvalid=entered_bedsvalid, joinsvalid=joinsvalid, xp_gainedvalid=xp_gainedvalid, skiny=skiny)
if __name__ == '__main__':
    app.run(debug=True)