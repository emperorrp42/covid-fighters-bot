#main.py for covid fighters bot

import discord
from discord.ext import commands
from disputils import BotEmbedPaginator
import gspread
import os

client=commands.Bot(command_prefix='=')
token = os.getenv("DISCORD_BOT_TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

gc = gspread.service_account(filename=GSERV_ACC)
ox_sheet = gc.open_by_key('16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM')
#oxygen resources sheet of cfi, bot only a viewer^

@client.command()
async def sheet(ctx):
    embed=discord.Embed(
        colour=discord.Colour.blurple()
    )
    embed.set_author(name='Covid Fighters Resources')
    embed.add_field(name='Primary Resource Sheet', value='https://docs.google.com/spreadsheets/d/1OL7go19rRpSdxemQXHM0cTBds2hjspj7_U7Ag7NdOCQ/edit#gid=92299482', inline=False)
    embed.add_field(name='Plasma', value='[Click here](https://docs.google.com/spreadsheets/d/1cbxCbhLVRWBlyRmzKuEQ-0PG3fsSs6EMIR51d2OoCIg/edit#gid=0)')
    embed.add_field(name='Oxygen', value='[Click here](https://docs.google.com/spreadsheets/d/16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM/edit?usp=sharing)')
    embed.add_field(name='Hospital Beds', value='[Click here](https://docs.google.com/spreadsheets/d/16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM/edit?usp=sharing)')
    embed.add_field(name='Medicines', value='[Click here](https://docs.google.com/spreadsheets/d/17bc83Sjnakb5DgsEQ7-lRj30-JVrIjSCcQuvwxB4Bc0/edit?usp=sharing)')
    embed.add_field(name='Food Resources', value='[Click here](https://docs.google.com/spreadsheets/d/12-0vEXzVTdVEi85snlFNoElym8hRW3ABvrbgxN0VjV8/edit?usp=sharing)')
    embed.add_field(name='Home Nurses', value='[Click here](https://docs.google.com/spreadsheets/d/1WLxv-GG-ANTajmnX9Kh4Gaa6-KffY5T1YljZI0ntVa4/edit?usp=sharing)')
    embed.add_field(name='Testing', value='[Click here](https://docs.google.com/spreadsheets/d/1ghFWQjrWP0XN5TitfbepDW3_yle_bJ-gFBRQZ8wMwsc/edit?usp=sharing)')
    embed.add_field(name='Ambulances', value='[Click here](https://docs.google.com/spreadsheets/d/1WtmVNMgmZs_NG9gshwL7FPRk3h4SB8yW8GJ2xOkI_WU/edit?usp=sharing)')
    embed.add_field(name='Other Resources/Helplines', value='[Click here](https://docs.google.com/spreadsheets/d/1OL7go19rRpSdxemQXHM0cTBds2hjspj7_U7Ag7NdOCQ/edit#gid=0)')
    embed.add_field(name='Doctors', value='[Click here](https://docs.google.com/spreadsheets/d/13l3jD-zVzkqKcXBOPCX5im14sdUYIfmZGw7jUtYe0iw/edit?usp=sharing)')
    embed.add_field(name='Mental Health Resources', value='[Click here](https://docs.google.com/spreadsheets/d/1I-90ogSH3S8hZHVCZ8T6BPzh8cB9XT-ykSLgZNytpH8/edit?usp=sharing)')
    embed.add_field(name='Whatsapp/Telegram Group', value='[Click here](https://docs.google.com/spreadsheets/d/1dyDTjj4DpTmVp4rB9KeIsa1x4lEp9Lvg1wmpAQnPgnY/edit?usp=sharing)')
    embed.add_field(name='Home ICU', value='[Click here](https://docs.google.com/spreadsheets/d/16pyViaSzEd0PCkAN98Z5fPdbBlOXQEtpdOnm4mgLBFU/edit?usp=sharing)')
    await ctx.send(embed=embed)

@client.command()
async def row1(ctx):
    worksheet = ox_sheet.get_worksheet(1)
    val = worksheet.acell('C9').value
    await ctx.send(val)

#accepting oxygen record as a 'list of dictionaries' then filtering oxygen leads by location, verified/unverified, etc
#'sought_value' is the keyword to be searched for and 'filtee' is the paramater (location, etc) in the head being filtered by
def filter(sought_value, filtee, sheet_num, sheet_key, head_num):
    current_sheet=gc.open_by_key(sheet_key)
    worksheet=current_sheet.get_worksheet(sheet_num)
    l_o_d = worksheet.get_all_records(empty2zero=False, head=head_num, default_blank='', allow_underscores_in_numeric_literals=False, numericise_ignore=None, value_render_option=None)
    found_values = []
    for dictionary in l_o_d:
        if (dictionary[filtee] == sought_value):
            found_values.append(dictionary)    
    #for dictionary in l_o_d: 
    return found_values

#test filter: fiter check
@client.command()
async def filter1(ctx):
    ab = []
    ab = filter('Delhi NCR', 'STATE', 1, '16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM', 7)
    a = ab[0]['STATUS']
    b = ab[0]['LOCATION (CITY)']
    c = ab[0]['CONTACT NUMBER']
    await ctx.send(a+', '+b+',\nContact num:'+str(c))

#test filter 2: embedding all matching leads consecutively
@client.command()
async def filter2(ctx):
    arr = []
    arr = filter('West Bengal', 'STATE', 1, '16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM', 7)
    a = 1
    embed = discord.Embed(
        colour = discord.Colour.blurple())
    embed.set_author(name="Test Filter2 Run:")
    embed.add_field(name='First field', value='Hello World', inline=False)
    leadloop1(arr, a, embed)
    await ctx.send(embed=embed)

def leadloop1(arr, a, arg2, filtee):
    #for dictionary in arr:
    embedx= discord.Embed(
            colour=discord.Colour.blurple()
        )
    embedx.set_author(name='Filtered leads for oxygen by ' + filtee + ': '+arg2)
    strname = 'Lead '+ str(a)
    a-=1
    strvalue1 = 'NAME: '+ arr[a]['NAME'] + '\nCONTACT NUMBER: '+str(arr[a]['CONTACT NUMBER'])
    strvalue2 = strvalue1 + '\nSTATE: '+ arr[a]['STATE'] + '\nLOCATION (CITY): '+arr[a]['LOCATION (CITY)']
    strvalue3 = strvalue2 + '\nSTATUS: '+arr[a]['STATUS'] + '\nUPDATE TIME: '+str(arr[a]['DATE AND TIME OF VERIFICATION (AUTOMATED; DO NOT EDIT)'])
    strvalue4 = strvalue3 + '\nPRICE: '+str(arr[a]['PRICE']) + '\nCYLINDER: '+arr[a]['CYLINDER']
    strvalue5 = strvalue4 + '\nCANS: '+arr[a]['CANS']+'\nREFILL: '+arr[a]['REFILL']
    strvalue6 = strvalue5 + '\nADDITIONAL INFO: '+arr[a]['ADDITIONAL INFO']
    embedx.add_field(name=strname, value=strvalue6, inline=False)
    embedx.set_footer(text='<- Navigate through by reacting to this message ->')
    a+=1
    return embedx

def leadloop2(arr, a, arg2, filtee):
    embedx= discord.Embed(
            colour=discord.Colour.blurple()
        )
    embedx.set_author(name='Filtered leads for hospital beds by ' + filtee + ': '+arg2)
    strname = 'Lead '+ str(a)
    a-=1
    strvalue1 = 'NAME: '+ arr[a]['Name of Hospital'] + '\nPHONE NUMBER: '+str(arr[a]['Phone Number'])
    strvalue2 = strvalue1 + '\nSTATE: '+ arr[a]['State'] + '\nCITY: '+arr[a]['City']
    strvalue3 = strvalue2 + '\nSTATUS: '+arr[a]['Status'] + '\nUPDATE TIME: '+str(arr[a]['Time of Verification (hh:mm AM/PM)'])
    strvalue4 = strvalue3 + '\nSPECIAL NOTES: '+str(arr[a]['Special Notes']) + '\nNO. OF BEDS WITH VENTILATOR '+str(arr[a]['Number of Beds with Ventilator'])
    strvalue5 = strvalue4 + '\nBEDS WITH OXYGEN: '+str(arr[a]['Beds with oxygen'])
    embedx.add_field(name=strname, value=strvalue5, inline=False)
    embedx.set_footer(text='<- Navigate through by reacting to this message ->')
    a+=1
    return embedx

def leadloop3(arr, a, arg2, filtee):
    embedx = discord.Embed(
        colour=discord.Colour.blurple()
    )
    embedx.set_author(name='Filtered leads for medicines by '+ filtee + ': '+arg2)
    strname = 'Lead '+str(a)
    a-=1
    strvalue1 = 'NAME: '+arr[a]['Name'] + '\nLOCATION: '+ arr[a]['Location'] 
    strvalue2 = strvalue1 + '\nMEDICINE: '+arr[a]['Medicine'] + '\nSTATE: '+ arr[a]['States ']
    strvalue3 = strvalue2 + '\nCONTACT: ' + str(arr[a]['Contact']) + '\nVERIFICATION: ' + arr[a]['Verification']
    strvalue4 = strvalue3+ '\nDATE/TIME OF VERIFICATION: ' + str(arr[a]['Date and Time of Verification'])
    strvalue5 = strvalue4+ '\nLINK/EMAIL: ' + arr[a]['Link/Email'] + '\nADDITIONAL INFO: ' + arr[a]['Additional Info']
    embedx.add_field(name=strname, value=strvalue5, inline=False)
    embedx.set_footer(text='<- Navigate through by reacting to this message ->')
    a+=1
    return embedx

@client.command()
async def oxygen(ctx, arg1, arg2):
    #arg 1 is filter type (filtee), arg 2 is sought value
    emoji1 = '◀️'
    emoji2 = '▶️'
    arr = []
    ox_key = '16Ez6gDbBHtIbZRkoe3h6yG4eZeERZZEZ_LzNQ-w1lpM'
    pagenum = 0
    no_of_leads = 0
    embeds = []
    a=1
    if (arg1=='nofilter'):
        #no filter, just get_all_records
        current_sheet=gc.open_by_key(ox_key)
        worksheet=current_sheet.get_worksheet(0)
        head_num = 8
        filtee = '(No Filter)'
        arr= worksheet.get_all_records(empty2zero=False, head=head_num, default_blank='', allow_underscores_in_numeric_literals=False, numericise_ignore=None, value_render_option=None)
        for dictionary in arr:
            embeds.append(leadloop1(arr, a, arg2, filtee))
            a+=1
    elif (arg1=='locfilter'):
        filtee = 'LOCATION (CITY)'
        arr = filter(arg2, filtee, 0, ox_key, 8)
        for dictionary in arr:
            embeds.append(leadloop1(arr, a, arg2, filtee))
            a+=1
    elif (arg1=='statusfilter'):
        filtee = 'STATUS'
        arr = filter(arg2, filtee, 0, ox_key, 8)
        for dictionary in arr:
            embeds.append(leadloop1(arr, a, arg2, filtee))
            a+=1
    elif (arg1=='statefilter'):
        filtee='STATE'
        arr = filter(arg2, filtee, 0, ox_key, 8)
        for dictionary in arr:
            embeds.append(leadloop1(arr, a, arg2, filtee))
            a+=1
    #msg = await ctx.send(embed=embed)
    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()
    
@client.command()
async def hospbeds(ctx, arg1, arg2):
    arr = []
    embeds = []
    a = 1
    hosp_key = '1KtDiUWbYtGVWf9gO4FN1AUUerexnsHyQYa0AiKmNE3k'
    if (arg1 == 'nofilter'):
        current_sheet=gc.open_by_key(hosp_key)
        worksheet=current_sheet.get_worksheet(0)
        head_num = 7
        filtee = '(No Filter)'
        arr= worksheet.get_all_records(empty2zero=False, head=head_num, default_blank='', allow_underscores_in_numeric_literals=False, numericise_ignore=None, value_render_option=None)
        for dictionary in arr:
            embeds.append(leadloop2(arr, a, arg2, filtee))
            a+=1
    if (arg1 == 'locfilter'):
        filtee = 'City'
        arr = filter(arg2, filtee, 0, hosp_key, 7)
        for dictionary in arr:
            embeds.append(leadloop2(arr, a, arg2, filtee))
            a+=1
    if (arg1 == 'statefilter'):
        filtee = 'State'
        arr = filter(arg2, filtee, 0, hosp_key, 7)
        for dictionary in arr:
            embeds.append(leadloop2(arr, a, arg2, filtee))
            a+=1
    if (arg1 == 'statusfilter'):
        filtee = 'Status'
        arr = filter(arg2, filtee, 0, hosp_key, 7)
        for dictionary in arr:
            embeds.append(leadloop2(arr, a, arg2, filtee))
            a+=1
    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()

@client.command()
async def medicine(ctx, arg1, arg2):
    arr = []
    embeds = []
    a = 1
    med_key = '17bc83Sjnakb5DgsEQ7-lRj30-JVrIjSCcQuvwxB4Bc0'
    head_num = 13
    if (arg1 == 'nofilter'):
        current_sheet = gc.open_by_key(med_key)
        worksheet = current_sheet.get_worksheet(1)
        filtee = '(No Filter)'
        arr= worksheet.get_all_records(empty2zero=False, head=head_num, default_blank='', allow_underscores_in_numeric_literals=False, numericise_ignore=None, value_render_option=None)
        for dictionary in arr:
            embeds.append(leadloop3(arr, a, arg2, filtee))
            a+=1
    if (arg1 == 'locfilter'):
        filtee = 'Location'
        arr = filter(arg2, filtee, 1, med_key, head_num)
        for dictionary in arr:
            embeds.append(leadloop3(arr, a, arg2, filtee))
            a+=1
    if (arg1 == 'medtype'):
        filtee ='Medicine'
        arr = filter(arg2, filtee, 1, med_key, head_num)
        for dictionary in arr:
            embeds.append(leadloop3(arr, a, arg2, filtee))
            a+=1
    if (arg1 == 'statefilter'):
        filtee = 'States '
        arr = filter(arg2, filtee, 1, med_key, head_num)
        for dictionary in arr:
            embeds.append(leadloop3(arr, a, arg2, filtee))
            a+=1
    if (arg1 == 'verfilter'):
        filtee = 'Verification'
        arr = filter(arg2, filtee, 1, med_key, head_num)
        for dictionary in arr:
            embeds.append(leadloop3(arr, a, arg2, filtee))
            a+=1
    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()

@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round (client.latency * 1000)}ms ')

#bot info dispenser (upon a hi or info command)
response = open('bot_info.txt').read()
@client.command()
async def hi(ctx):
    await ctx.send(response)
@client.command()
async def about(ctx):
    await ctx.send(response)

#in case an error occurs:
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f'Error. Try =help for available commands ({error})')

#help (list of possible commands)
client.remove_command('help')
@client.command()
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.blurple())
    embed.set_author(name="Current available commands: ")
    #embed.set_thumbnail(url='something')
    embed.add_field(name='=ping', value='Check latency', inline=False)
    embed.add_field(name='=hi/=about', value="About this bot", inline=False)
    embed.add_field(name='=help', value='Display list of commands', inline=False)
    #embed.add_field(name='=invite', value='Get this bot invite link to add to a server', inline=False)
    embed.add_field(name='=sheet', value='Links to the resource sheets', inline=False)
    stroxhelp = '=oxygen nofilter none for viewing all leads\n=oxygen locfilter (name of city) for filtering by city\n=oxygen statefilter (name of state) for filtering by state\n=oxygen statusfilter (Available/Unavailable/Needs Verification)'
    embed.add_field(name='=oxygen (type of filter) (argument for filter)', value='Displays filtered leads for oxygen from the "Sheet for Users" of the CFI Oxygen resources sheet\n'+stroxhelp+'\n(NOTE: enter multi-word arguments within double quotes("...")', inline=False)
    strbedhelp = '=hospbeds nofilter none for viewing all leads\n=hospbeds locfilter (name of city) for filtering by city\n=hospbeds statefilter (name of state) for filtering by state\n=hospbeds statusfilter (Beds Available/Not Responding/Call to Check Soon/Beds Not Available'
    embed.add_field(name='=hospbeds (type of filter) (argument for filter)', value='Displays filtered leads for hospital beds from the CFI Hospital Beds resources sheet\n'+strbedhelp+'\n(NOTE: enter multi-word arguments within double quotes("...")', inline=False)
    strmedhelp = '=medicine nofilter none for viewing all leads\n=medicine locfilter (address/location) for filtering by location\n=medicine statefilter (name of state) for filtering by state\n=medicine medfilter (name of medicine) for filtering by name of medicine\n'
    strmedhelp2 = strmedhelp+ '=medicine verfilter ("NOT WORKING/OUT OF STOCK/ SWITCHED OFF/ INVALID","Available","BUSY/RINGING/NOT PICKING UP") for filtering by verification status'
    embed.add_field(name='=medicine (type of filter) (argument for filter)', value='Displays filtered leads for medicines from the CFI medicines resource sheet\n'+strmedhelp2 + '\n(NOTE: enter multi-word arguments within double quotes("...")', inline=False)
    embed.set_footer(text= 'More commands coming soon')
    #embed.add_field(name='=addlead {name of lead}', value='Add a lead and enter relevant details')
    await ctx.send(embed=embed)

client.run(token)