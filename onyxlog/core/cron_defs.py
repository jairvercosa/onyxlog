# -*- coding: ISO-8859-1 -*-
import calendar
from datetime import datetime

def execCronTasks():
    hoje = datetime.today()

    if hoje.day == 1:
        
        lastDayMonth = {
            "day": hoje.day,
            "month": hoje.month,
            "year": hoje.year
        }

        #pega mes anterior
        if lastDayMonth['month'] == 1:
            lastDayMonth['month'] = 12
            lastDayMonth['year'] -= 1
        else:
            lastDayMonth['month'] -= 1

        lastDayMonth['day'] = calendar.monthrange(lastDayMonth['year'],lastDayMonth['month'])[1]
        lastDay = datetime.strptime(
            str(lastDayMonth['year'])+"-"+str(lastDayMonth['month'])+"-"+str(lastDayMonth['day'])
            ,'%Y-%m-%d')

    else:
        lastDay = hoje

    cron_snapshot_equipe(lastDay)
    cron_snapshot_meta(str(lastDay.month).zfill(2), lastDay)

    return True

def cron_snapshot_equipe(dataSnapshot):
    """
    Realiza snapshot da base de dados para informações retroativas de membros de equipe.
    Basta executar a rotina e ela irá tirar uma fotografia no momento atual da equipe.
    """
    from onyxlog.equipe.models.membro import Membro
    from onyxlog.equipe.models.snapshotequipe import SnapshotEquipe
    from onyxlog.equipe.models.snapshotequipeitem import SnapshotEquipeItem

    membros = Membro.objects.all()
    if not membros:
        return True

    #Cria cabeçalho SnapShot
    snapShot = SnapshotEquipe(data=dataSnapshot)
    snapShot.save()

    for membro in membros:
        snapShotItem = SnapshotEquipeItem(
            snapshot = snapShot,
            membroId = membro.pk,
            criador  = membro.criador,
            usuario  = membro.usuario,
            liderId  = None if not membro.lider else membro.lider.id,
            criado   = membro.criado,
        )
        snapShotItem.save()

        carteiras = membro.carteiras.all()
        for carteira in carteiras:
            snapShotItem.carteiras.add(carteira)
            snapShotItem.save()

    return True

def cron_snapshot_meta(monthMeta, dataSnapshot):
    """
    Realiza snapshot da base de dados para informações retroativas de metas de membros de equipe.
    Basta executar a rotina e ela irá tirar uma fotografia no momento atual das metas.
    """
    from onyxlog.equipe.models.membrometa import MembroMeta
    from onyxlog.equipe.models.snapshotmeta import SnapshotMeta
    from onyxlog.equipe.models.snapshotmetaitem import SnapshotMetaItem

    if not monthMeta:
        return False

    membrosMeta = MembroMeta.objects.filter(mesVigencia=monthMeta)
    if not membrosMeta:
        return True

    #Cria cabeçalho SnapShot
    snapShot = SnapshotMeta(data=dataSnapshot)
    snapShot.save()

    for meta in membrosMeta:
        snapShotItem = SnapshotMetaItem(
            snapshot    = snapShot,
            criador     = meta.criador,
            metaId      = meta.pk,
            membroId    = meta.membro.id,
            tipometa    = meta.tipometa,
            receita     = meta.receita,
            valor       = meta.valor,
            mesVigencia = meta.mesVigencia,
            anoVigencia = meta.anoVigencia,
            criado      = meta.criado,
            is_Visible  = meta.is_Visible,
        )
        snapShotItem.save()

    return True

