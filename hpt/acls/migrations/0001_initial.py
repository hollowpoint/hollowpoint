# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccessList'
        db.create_table(u'acls_accesslist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'acls', ['AccessList'])

        # Adding M2M table for field devices on 'AccessList'
        m2m_table_name = db.shorten_name(u'acls_accesslist_devices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('accesslist', models.ForeignKey(orm[u'acls.accesslist'], null=False)),
            ('netdevice', models.ForeignKey(orm[u'inventory.netdevice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['accesslist_id', 'netdevice_id'])


    def backwards(self, orm):
        # Deleting model 'AccessList'
        db.delete_table(u'acls_accesslist')

        # Removing M2M table for field devices on 'AccessList'
        db.delete_table(db.shorten_name(u'acls_accesslist_devices'))


    models = {
        u'acls.accesslist': {
            'Meta': {'object_name': 'AccessList'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'devices': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'acls'", 'symmetrical': 'False', 'to': u"orm['inventory.NetDevice']"}),
            'filename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'})
        },
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
            'Meta': {'object_name': 'NetDevice'},
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
            'layer2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'layer3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'layer4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
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

    complete_apps = ['acls']