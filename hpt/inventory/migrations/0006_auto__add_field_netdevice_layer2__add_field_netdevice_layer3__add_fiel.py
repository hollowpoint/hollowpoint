# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NetDevice.layer2'
        db.add_column(u'inventory_netdevice', 'layer2',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'NetDevice.layer3'
        db.add_column(u'inventory_netdevice', 'layer3',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'NetDevice.layer4'
        db.add_column(u'inventory_netdevice', 'layer4',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NetDevice.layer2'
        db.delete_column(u'inventory_netdevice', 'layer2')

        # Deleting field 'NetDevice.layer3'
        db.delete_column(u'inventory_netdevice', 'layer3')

        # Deleting field 'NetDevice.layer4'
        db.delete_column(u'inventory_netdevice', 'layer4')


    models = {
        u'djcelery.taskstate': {
            'Meta': {'ordering': "[u'-tstamp']", 'object_name': 'TaskState'},
            'args': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'eta': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'db_index': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'retries': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'runtime': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'traceback': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'tstamp': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djcelery.WorkerState']", 'null': 'True'})
        },
        u'djcelery.workerstate': {
            'Meta': {'ordering': "[u'-last_heartbeat']", 'object_name': 'WorkerState'},
            'hostname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_heartbeat': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'})
        },
        u'inventory.netdevice': {
            'Meta': {'ordering': "('node_name',)", 'object_name': 'NetDevice'},
            'OOBTerminalServerConnector': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'OOBTerminalServerFQDN': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'OOBTerminalServerNodeName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'OOBTerminalServerPort': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'OOBTerminalServerTCPPort': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'adminStatus': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'assetID': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'authMethod': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'barcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'budgetCode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'budgetName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'coordinate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'deviceType': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'enablePW': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layer2': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'layer3': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'layer4': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lifecycleStatus': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'loginPW': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'nodePort': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'node_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'onCallEmail': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'onCallID': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'onCallName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'operationStatus': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'owningTeam': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'projectName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'serialNumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'devices'", 'symmetrical': 'False', 'to': u"orm['djcelery.TaskState']"})
        }
    }

    complete_apps = ['inventory']