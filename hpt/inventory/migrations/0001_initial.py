# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NetDevice'
        db.create_table(u'inventory_netdevice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('adminStatus', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('assetID', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('authMethod', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('barcode', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('budgetCode', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('budgetName', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('coordinate', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('deviceType', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('enablePW', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('lastUpdate', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('layer2', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('layer3', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('layer4', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('lifecycleStatus', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('loginPW', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('make', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('nodeName', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('nodePort', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('onCallEmail', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('onCallID', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('onCallName', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('operationStatus', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('owner', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('owningTeam', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('projectName', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('room', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('serialNumber', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('site', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('OOBTerminalServerConnector', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('OOBTerminalServerFQDN', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('OOBTerminalServerNodeName', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('OOBTerminalServerPort', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('OOBTerminalServerTCPPort', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['NetDevice'])


    def backwards(self, orm):
        # Deleting model 'NetDevice'
        db.delete_table(u'inventory_netdevice')


    models = {
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
            'deviceType': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'enablePW': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastUpdate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'layer2': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'layer3': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'layer4': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'lifecycleStatus': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'loginPW': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'nodeName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'nodePort': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'onCallEmail': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'onCallID': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'onCallName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'operationStatus': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'owningTeam': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'projectName': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'serialNumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'site': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['inventory']