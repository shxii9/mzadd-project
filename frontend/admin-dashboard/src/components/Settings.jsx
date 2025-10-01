import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Save, Shield, Bell, Globe, DollarSign } from 'lucide-react'

const Settings = () => {
  const [settings, setSettings] = useState({
    siteName: 'BidFlow',
    siteDescription: 'منصة المزادات الإلكترونية الرائدة في الكويت',
    commissionRate: 5,
    enableNotifications: true,
    enableEmailNotifications: true,
    maintenanceMode: false,
    autoApproveItems: false
  })

  const handleSave = () => {
    console.log('Saving settings:', settings)
    // Implement save functionality
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">إعدادات النظام</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-1">إدارة إعدادات المنصة العامة</p>
      </div>

      <Tabs defaultValue="general" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="general">عام</TabsTrigger>
          <TabsTrigger value="business">الأعمال</TabsTrigger>
          <TabsTrigger value="notifications">الإشعارات</TabsTrigger>
          <TabsTrigger value="security">الأمان</TabsTrigger>
        </TabsList>

        <TabsContent value="general" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Globe className="w-5 h-5" />
                <span>الإعدادات العامة</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="siteName">اسم الموقع</Label>
                <Input
                  id="siteName"
                  value={settings.siteName}
                  onChange={(e) => setSettings({...settings, siteName: e.target.value})}
                />
              </div>
              <div>
                <Label htmlFor="siteDescription">وصف الموقع</Label>
                <Input
                  id="siteDescription"
                  value={settings.siteDescription}
                  onChange={(e) => setSettings({...settings, siteDescription: e.target.value})}
                />
              </div>
              <div className="flex items-center space-x-2">
                <Switch
                  id="maintenanceMode"
                  checked={settings.maintenanceMode}
                  onCheckedChange={(checked) => setSettings({...settings, maintenanceMode: checked})}
                />
                <Label htmlFor="maintenanceMode">وضع الصيانة</Label>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="business" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <DollarSign className="w-5 h-5" />
                <span>إعدادات الأعمال</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="commissionRate">معدل العمولة (%)</Label>
                <Input
                  id="commissionRate"
                  type="number"
                  value={settings.commissionRate}
                  onChange={(e) => setSettings({...settings, commissionRate: parseFloat(e.target.value)})}
                />
              </div>
              <div className="flex items-center space-x-2">
                <Switch
                  id="autoApproveItems"
                  checked={settings.autoApproveItems}
                  onCheckedChange={(checked) => setSettings({...settings, autoApproveItems: checked})}
                />
                <Label htmlFor="autoApproveItems">الموافقة التلقائية على السلع</Label>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Bell className="w-5 h-5" />
                <span>إعدادات الإشعارات</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center space-x-2">
                <Switch
                  id="enableNotifications"
                  checked={settings.enableNotifications}
                  onCheckedChange={(checked) => setSettings({...settings, enableNotifications: checked})}
                />
                <Label htmlFor="enableNotifications">تفعيل الإشعارات</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Switch
                  id="enableEmailNotifications"
                  checked={settings.enableEmailNotifications}
                  onCheckedChange={(checked) => setSettings({...settings, enableEmailNotifications: checked})}
                />
                <Label htmlFor="enableEmailNotifications">إشعارات البريد الإلكتروني</Label>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Shield className="w-5 h-5" />
                <span>إعدادات الأمان</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                إعدادات الأمان متقدمة ويتم إدارتها من خلال ملفات التكوين
              </p>
              <Button variant="outline">
                عرض سجل الأمان
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <div className="flex justify-end">
        <Button onClick={handleSave} className="flex items-center space-x-2">
          <Save className="w-4 h-4" />
          <span>حفظ الإعدادات</span>
        </Button>
      </div>
    </div>
  )
}

export default Settings
