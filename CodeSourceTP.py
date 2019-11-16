import tkinter

class Instruction:
    si=None
    x=None
    sf=None
    def __init__(self,si,x,sf):
        self.si=si
        self.sf=sf
        self.x=x

class Automate:
    Instructions = []
    EF = []
    S0= []
    S=[]
    X=[]
    def __init__(self,instrs,EF,s0):
        self.S0=s0
        self.EF=EF
        self.Instructions=instrs
        for i in instrs:
            if i.si not in self.S:
                self.S.append(i.si)
            if i.sf not in self.S:
                self.S.append(i.sf)
            if i.x not in self.X:
                self.X.append(i.x)

    def fils(self,etat):
        l = []
        for i in self.Instructions:
            if i.si==etat :
                 l.append(i.sf)
        return l

    def automateSimple(self):
        automate= Automate(self.Instructions[:],self.EF[:],self.S0[:])
        automate.S=self.S[:]
        indice=0
        while indice  < len(automate.Instructions):
            i=automate.Instructions[indice]
            if len(i.x)>1 :
                automate.Instructions.remove(i)
                indice-=1
                tmp=i.si
                for c in i.x[:len(i.x)-1]:
                    nv='s'+str(len(automate.S))
                    automate.Instructions.append(Instruction(tmp,c,nv))
                    automate.S.append(nv)
                    tmp=nv
                automate.Instructions.append(Instruction(tmp,i.x[len(i.x)-1], i.sf))
            if i.x=='' :
                automate.Instructions.remove(i)
                if i.sf in automate.EF:
                    if i.si not in automate.EF:
                        automate.EF.append(i.si)
                    if not any(instre.sf==i.sf for instre in automate.Instructions):
                        automate.EF.remove(i.sf)

                indice-=1
                ind=0
                while ind < len(automate.Instructions):
                    instruction=automate.Instructions[ind]
                    if instruction.si==i.sf :
                        if not ((i.si==instruction.sf) and (instruction.x=='')) :
                            automate.Instructions.append(Instruction(i.si,instruction.x,instruction.sf))
                    ind+=1
            indice+=1
        return automate

    def automateReduit(self):
        arr=[]
        for tmp in self.S0 :
            arr.append(tmp)
        i=0
        while (i<len(arr)):
            sF=self.fils(arr[i])
            for f in sF :
                if self.coacc(f) and f not in arr : arr.append(f)
            i=i+1
        ins=[]
        for i in self.Instructions:
            if i.si in arr and i.sf in arr :
                ins.append(i)
        return  Automate(ins,self.EF,self.S0)
    def coacc(self,etat):
        if etat in self.EF:
            return True
        F=self.fils(etat)
        if len(F)==0:
            return False
        a=False
        for f in F:
            a=a | self.coacc(f)
        return a
    def reconMot(self,mot):
        auto=self.automateSimple()
        class trans:
            s = None
            pred = None
            def __init__(self, s, pred):
                self.s = s
                self.pred = pred

        for s0 in auto.S0:
            find=False
            arr = [[trans(s0,'')]]
            for i in range(len(mot)):
                arr.append([])
            indice=0
            for x in mot:
                for ar in arr[indice]:
                    tmp=list(filter(lambda instr: instr.si==ar.s and instr.x==x,auto.Instructions[:]))
                    for etat in tmp :
                        arr[indice+1].append(trans(etat.sf,ar.s))
                if len(arr[indice+1])==0: break
                indice+=1
            f=list(filter(lambda x : x.s in auto.EF ,arr[len(mot)]))
            if(len(f)!=0):
                find=True
                break
        chemin=[]
        if find :
            chemin = [f[0].s,f[0].pred]
            s = f[0].pred
            for i in range(len(mot)-1,-1,-1):
                f = list(filter(lambda x: x.s == s, arr[i]))
                s=f[0].pred
                chemin.append(s)
        chemin.reverse()
        return  [find,chemin[1:]]

    def automateDeterministe(self):
        # still reglage de tableau detat
        selfAuto = self.automateSimple()
        automate=Automate([],selfAuto.EF[:],selfAuto.S0[:])
        qr=[]
        start=selfAuto.S0[:]
        for etat in start:
            tmpArr=[]
            if str(etat)!=etat:
                for ata in etat:
                    tmpArr+=list(filter(lambda instr: instr.si==ata,selfAuto.Instructions[:]))
            tmpArr+=list(filter(lambda instr: instr.si==etat,selfAuto.Instructions[:]))
            xarr=set([tmpArr[i].x for i in range(len(tmpArr))])
            for x in xarr :
                xInstr = list(filter(lambda instr: instr.x == x, tmpArr))
                if len(xInstr) > 1 :
                    xEtat=[xInstr[i].sf for i in range(len(xInstr))]
                    for final in xEtat:
                            if (final in automate.EF ):
                                automate.EF.append(xEtat)
                                break
                elif len(xInstr) == 1 : xEtat=xInstr[0].sf
                qr.append(Instruction(etat,x,xEtat))
                if xEtat not in start : start.append(xEtat)
        return Automate(qr,automate.EF,automate.S0)
    def automateComplement(self):
        auto=Automate(self.Instructions[:],self.EF[:],self.S0[:])
        for etat in auto.S :
            for x in auto.X :
                if(not any(i.x==x and i.si==etat for i in self.Instructions)) :
                    auto.Instructions.append(Instruction(etat,x,'Puis'))
            if etat in auto.EF : auto.EF.remove(etat)
            else : auto.EF.append(etat)
        auto.S.append('Puis')
        auto.EF.append('Puis')
        return auto
    def automateMirroir(self):
        instrs=[]
        EF=[]
        S0=[]
        for i in self.Instructions :
            instrs.append(Instruction(i.sf,i.x,i.si))
        for etat in self.S:
            if etat in self.EF and etat not in self.S0:
                S0.append(etat)
            if etat in self.S0 and etat not in self.EF:
                EF.append(etat)
        return Automate(instrs,EF,S0)

def createAutomateFichier():
    f = open("fich.txt", "r")
    f.readline()
    f.readline()
    f.readline()
    l=f.readline()
    s = l[:-1].split(',')
    f.readline()
    f.readline()
    l = f.readline()
    sa = l[:-1].split(',')
    sa.append('')
    f.readline()
    f.readline()
    l = f.readline()
    try:
        n = int(l[:-1])

    except ValueError:
        print('le nombre de transitions n\'est pas entier')
        return [False, None]

    ins = []
    f.readline()
    f.readline()
    b = True
    for i in range(n):
            l = f.readline()
            if l == '':
                print("il ya des lignes vides dans le fichier")
                return [False, None]
            trans = l[:-1].split(',')
            for x in trans[1]:
                if x not in sa:
                    b = False
                    print(x," n'est pas dans l'ensemble d'alphabet")
                    return [False, None]
                    break
            if not (trans[0] in s and trans[2] in s):
                print("il y a des transitions qui contient des etats qui  ne sont pas dans l'ensemble des etats")
                return [False, None]
                break
            else:
                ins.append(Instruction(trans[0], trans[1], trans[2]))
    f.readline()
    f.readline()
    l = f.readline()
    ef = l[:-1].split(',')
    if any(i not in s for i in ef):
        b=False
        print("quelque états finaux  ne sont pas dans l'ensemble des etats")
        return [False, None]
    f.readline()
    f.readline()
    l = f.readline()
    e =  l[:-1].split(',')
    if any(i not in s for i in e):
        b=False
        print("quelque états initinaux  ne sont pas dans l'ensemble des etats")
        return [False, None]
    return  [b,Automate(ins, ef, e)]

auto = None
print('TP THP\n\n')
print('consulter l\'aide d\'utilisation')
while(True):
    print("Veuillez choisir un choix")
    print('0-créer automate a partir d\'un fichier')
    print('1-créer automate a partir le console')
    print('2-vérifier si un mot est connu par l\'automate')
    print('3-voir l\'automate simple de cet automate')
    print('4-voir l\'automate déterministe de cet automate')
    print('5-voir l\'automate réduit de cet automate')
    print('6-voir l\'automate mirroir de cet automate')
    print('7-voir l\'automate complément de cet automate')
    print("8-afficher votre automate")
    print('9-supprimemer l\'automate')
    print("10-exit")
    choix  = input()
    if choix == '0':
        if auto==None:
            print("remplir le fichier fich.txt a partir du format spécifiée dans le fichier")
            auto=createAutomateFichier()
            if auto[0] :
                print("l'automate est crée")
                auto=auto[1]
            else:
                print("réssayer")
                break;
        else:
            print("l'automate est déja créé si vous voulez créer un autre automate supprimmer le premier d'abor a partir de menu")
        print("appuyez sur une button pour revenir au menu")
        input()
    if choix =='1' :
        if auto == None :
            print("entrer les états de votre automate de cette façons s1,s2,s3,.....etc")
            s = input().split(',')
            print("entrer l'alphabet de votre automate de cette façons a,b,c,.....etc")
            sa = input().split(',')
            sa.append('')
            print("veuillez entrer le nombre des transitions de votre automate")
            # try catch
            while True:
                try:
                    n = int(input())
                    break
                except ValueError:
                    print('Please enter an integer')

            ins = []
            print(
                "veuillez entrer les transitions de votre automate de cette façon \n Si,x,Sf telle que Si et Sf les noms des états du départ et d'arrivé")
            for i in range(n):
                print("entrer transition numero ", i + 1, '\n')
                while True:
                    trans = input().split(',')
                    bool = True
                    for x in trans[1]:
                        if x not in sa:
                            bool = False
                    if not (trans[0] in s and trans[2] in s and bool):
                        print(
                            "la transition que vous avez entrer est erronée une des états n'existe pas de l'ensemble des etats \n ou le mot n'existe pas dans l'ensemble des alphabet")
                    else:
                        ins.append(Instruction(trans[0], trans[1], trans[2]))
                        break

            print("entrer les etats finies dans cette forme : s1,s2,... (les noms des états séparés par ,)")
            while True:
                f = input().split()
                if any(i not in s for i in f) :
                    print("les etats que vous avez entrer n'exsitent pas")
                else:
                    break
            print("entrer les etats initiales dans cette forme : s1,s2,... (les noms des états séparés par ,)")
            while True:
                e = input().split()
                if any(i not in s for i in e) :
                    print("les etats que vous avez entrer n'exsitent pas")
                else:
                    break


            auto = Automate(ins, f, e)
        else:
            print("l'automate est déja créé si vous voulez créer un autre automate supprimmer le premier d'abor a partir de menu")
        print("appuyez sur une button pour revenir au menu")
        input()
    elif choix == '5' :
        if auto != None :
            automate=auto.automateReduit()
            print('le nouveaux automate')
            for ins in automate.Instructions:
                print(ins.si,' ',ins.x,' ',ins.sf)
            print("les etats finaux : ",automate.EF)
            print("les etats initiaux : ",automate.S0)
            automate=None
        else:
            print("vous n'avez pas créer l'automate")
        print("appuyez sur une button pour revenir au menu")
        input()
    elif choix == '3':
        if auto != None :
            automate = auto.automateSimple()
            print('le nouveaux automate')
            for ins in automate.Instructions:
                print(ins.si, ' ', ins.x, ' ', ins.sf)
            print("les etats finaux : ", automate.EF)
            print("les etats initiaux : ", automate.S0)
            print(len(automate.S))
            automate = None
        else:
            print("vous n'avez pas créer l'automate")
        print("appuyez sur une button pour revenir au menu")
        input()
    elif choix =='4':
        if auto != None :
            automate = auto.automateDeterministe()
            print('le nouveaux automate')
            for ins in automate.Instructions:
                print(ins.si, ' ', ins.x, ' ', ins.sf)
            print("les etats finaux : ", automate.EF)
            print("les etats initiaux : ", automate.S0)
            automate = None
        else:
            print("vous n'avez pas créer l'automate")
        print("appuyez sur une button pour revenir au menu")
        input()
    elif choix == '2':
        while True :
            if auto != None :
                print("entrer le mot")
                mot=input()
                print(auto.reconMot(mot))
            else:
                print("veuillez d'abord créer l'automate")
            print("appuyez sur une 'y' pour vérifier pour un autre mot ou n'importe quelle autre button pour revenir au menu")
            if input()!='y' : break
    elif choix =='6' :
        if auto != None :
            automate = auto.automateMirroir()
            print('le nouveaux automate')
            for ins in automate.Instructions:
                print(ins.si, ' ', ins.x, ' ', ins.sf)
            print("les etats finaux : ", automate.EF)
            print("les etats initiaux : ", automate.S0)
            automate = None
        else:
            print("vous n'avez pas créer l'automate")
        print("appuyez sur une button pour revenir au menu")
        input()
    elif choix =='7' :
        if auto != None :
            automate = auto.automateComplement()
            print('le nouveaux automate')
            for ins in automate.Instructions:
                print(ins.si, ' ', ins.x, ' ', ins.sf)
            print("les etats finaux : ", automate.EF)
            print("les etats initiaux : ", automate.S0)
            automate = None
        else:
            print("vous n'avez pas créer l'automate")
        print("appuyez sur une button pour revenir au menu")
        input()
    elif choix =='8' :
        if auto != None :
            automate=auto
            for ins in automate.Instructions:
                print(ins.si,' ',ins.x,' ',ins.sf)
            print("les etats finaux : ",automate.EF)
            print("les etats initiaux : ",automate.S0)
            automate = None
        else:
            print("veuillez d'abord créer l'automate")
        print("appuyez sur une button pour revenir au menu")
        input()
    elif choix=='9':
        auto=None
        print("l'automate est supprimé appuyez sur une button pour revenir au menu")
        input()
    elif choix == '10' :
        break
    else:
        print("vous devez entrer un numero entre 1 et 10\nappuyez sur une button pour revenir au menu")
        input()
input()