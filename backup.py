from structure import structure

backup_service = structure.instantiate('backup_service')


if __name__ == '__main__':
    backup_service.backup()
    backup_service.clean_up()
