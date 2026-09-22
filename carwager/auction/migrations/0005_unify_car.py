from django.db import migrations, models


def copy_auction_to_showbill(apps, schema_editor):
    # Historical models
    Auction = apps.get_model('auction', 'Auction')
    CarAuction = apps.get_model('auction', 'CarAuction')
    CarMarkAuction = apps.get_model('auction', 'CarMarkAuction')
    CarModelAuction = apps.get_model('auction', 'CarModelAuction')

    CarMark = apps.get_model('showbill', 'CarMark')
    CarModel = apps.get_model('showbill', 'CarModel')
    Car = apps.get_model('showbill', 'Car')

    db_alias = schema_editor.connection.alias

    # Map existing CarAuction entries to showbill.Car
    for car_auction in CarAuction.objects.using(db_alias).all():
        # Get auction mark/model strings
        mark_auction = CarMarkAuction.objects.using(db_alias).get(id=car_auction.mark_id)
        model_auction = CarModelAuction.objects.using(db_alias).get(id=car_auction.model_id)

        # Find or create canonical CarMark/CarModel in showbill
        mark_obj, _ = CarMark.objects.using(db_alias).get_or_create(car_mark=mark_auction.car_mark)
        model_obj, _ = CarModel.objects.using(db_alias).get_or_create(car_mark=mark_obj, car_model=model_auction.car_model)

        # Find or create Car
        car_obj, _ = Car.objects.using(db_alias).get_or_create(mark=mark_obj, model=model_obj, defaults={'year': car_auction.year})

        # Assign all auctions that pointed to this CarAuction to point to car_new
        Auction.objects.using(db_alias).filter(car_id=car_auction.id).update(car_new_id=car_obj.id)


def noop_reverse(apps, schema_editor):
    # No-op reverse: cannot reliably revert data migration
    pass


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('auction', '0004_remove_auction_image'),
        ('showbill', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='car_new',
            field=models.ForeignKey(null=True, on_delete=models.deletion.CASCADE, related_name='auctions', to='showbill.Car'),
        ),
        migrations.RunPython(copy_auction_to_showbill, reverse_code=noop_reverse),
        migrations.RemoveField(
            model_name='auction',
            name='car',
        ),
        migrations.RenameField(
            model_name='auction',
            old_name='car_new',
            new_name='car',
        ),
        migrations.AlterField(
            model_name='auction',
            name='car',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='auctions', to='showbill.Car'),
        ),
    ]
