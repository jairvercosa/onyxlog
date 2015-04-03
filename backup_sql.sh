#!/bin/bash

#################### SCRIPT PARA BACKUP MYSQL ####################
# Jeferson R. Costa <rc.jeferson@gmail.com>                      #
# Created Feb, 2013                                              #
# Update Feb, 2013                                               #

# Definindo parametros do MySQL
echo "  -- Definindo parametros do MySQL ..."
DB_NAME='onyxlog'
DB_USER='root'
DB_PASS=''
DB_PARAM='--add-drop-table --add-locks --extended-insert --single-transaction -quick'

# Definindo parametros do sistema
echo "  -- Definindo parametros do sistema ..."
DATE=`date +%Y-%m-%d`
MYSQLDUMP=/usr/bin/mysqldump
BACKUP_DIR=/onyxlog/backup
BACKUP_NAME=mysql-$DATE.sql
BACKUP_TAR=mysql-$DATE.tar

#Gerando arquivo sql
echo "  -- Gerando Backup da base de dados $DB_NAME em $BACKUP_DIR/$BACKUP_NAME ..."
$MYSQLDUMP $DB_NAME $DB_PARAM -u $DB_USER -p$DB_PASS > $BACKUP_DIR/$BACKUP_NAME

# Compactando arquivo em tar
echo "  -- Compactando arquivo em tar ..."
tar -cf $BACKUP_DIR/$BACKUP_TAR -C $BACKUP_DIR $BACKUP_NAME

# Compactando arquivo em bzip2
echo "  -- Compactando arquivo em bzip2 ..."
bzip2 $BACKUP_DIR/$BACKUP_TAR

# Excluindo arquivos desnecessarios
echo "  -- Excluindo arquivos desnecessarios ..."
rm -rf $BACKUP_DIR/$BACKUP_NAME