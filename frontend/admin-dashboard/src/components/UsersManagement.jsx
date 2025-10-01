import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Users, 
  Search, 
  Filter, 
  Plus, 
  Edit, 
  Trash2, 
  Eye, 
  Ban, 
  CheckCircle,
  Mail,
  Phone,
  Calendar,
  MoreHorizontal,
  UserPlus,
  Shield,
  Store,
  Gavel as GavelIcon
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table'
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuLabel, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from '@/components/ui/dropdown-menu'
import { 
  Dialog, 
  DialogContent, 
  DialogDescription, 
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from '@/components/ui/dialog'
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'

const UsersManagement = () => {
  const [users, setUsers] = useState([
    {
      id: 1,
      username: 'ahmed_merchant',
      email: 'ahmed@example.com',
      role: 'merchant',
      full_name: 'أحمد محمد الكندري',
      phone: '+965 9999 9999',
      is_active: true,
      is_verified: true,
      created_at: '2024-01-15',
      last_login: '2024-01-20',
      total_items: 15,
      total_auctions: 12,
      total_earnings: 2500.50
    },
    {
      id: 2,
      username: 'sara_bidder',
      email: 'sara@example.com',
      role: 'bidder',
      full_name: 'سارة أحمد العتيبي',
      phone: '+965 8888 8888',
      is_active: true,
      is_verified: true,
      created_at: '2024-01-10',
      last_login: '2024-01-21',
      total_bids: 45,
      won_auctions: 8
    },
    {
      id: 3,
      username: 'mohammed_store',
      email: 'mohammed@example.com',
      role: 'merchant',
      full_name: 'محمد خالد الرشيد',
      phone: '+965 7777 7777',
      is_active: false,
      is_verified: false,
      created_at: '2024-01-18',
      last_login: '2024-01-19',
      total_items: 3,
      total_auctions: 1,
      total_earnings: 150.00
    }
  ])

  const [filteredUsers, setFilteredUsers] = useState(users)
  const [searchTerm, setSearchTerm] = useState('')
  const [roleFilter, setRoleFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')
  const [selectedUser, setSelectedUser] = useState(null)
  const [showUserDialog, setShowUserDialog] = useState(false)
  const [showAddUserDialog, setShowAddUserDialog] = useState(false)

  // Filter users based on search and filters
  useEffect(() => {
    let filtered = users.filter(user => {
      const matchesSearch = user.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           user.email.toLowerCase().includes(searchTerm.toLowerCase())
      
      const matchesRole = roleFilter === 'all' || user.role === roleFilter
      const matchesStatus = statusFilter === 'all' || 
                           (statusFilter === 'active' && user.is_active) ||
                           (statusFilter === 'inactive' && !user.is_active) ||
                           (statusFilter === 'verified' && user.is_verified) ||
                           (statusFilter === 'unverified' && !user.is_verified)
      
      return matchesSearch && matchesRole && matchesStatus
    })
    
    setFilteredUsers(filtered)
  }, [users, searchTerm, roleFilter, statusFilter])

  const getRoleIcon = (role) => {
    switch (role) {
      case 'admin': return Shield
      case 'merchant': return Store
      case 'bidder': return GavelIcon
      default: return Users
    }
  }

  const getRoleBadge = (role) => {
    const colors = {
      admin: 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400',
      merchant: 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400',
      bidder: 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
    }
    
    const labels = {
      admin: 'مدير',
      merchant: 'تاجر',
      bidder: 'مزايد'
    }
    
    return (
      <Badge className={colors[role]}>
        {labels[role]}
      </Badge>
    )
  }

  const getStatusBadge = (user) => {
    if (!user.is_active) {
      return <Badge variant="destructive">معطل</Badge>
    }
    if (!user.is_verified) {
      return <Badge variant="secondary">غير مؤكد</Badge>
    }
    return <Badge variant="default" className="bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">نشط</Badge>
  }

  const handleUserAction = (action, userId) => {
    switch (action) {
      case 'activate':
        setUsers(prev => prev.map(user => 
          user.id === userId ? { ...user, is_active: true } : user
        ))
        break
      case 'deactivate':
        setUsers(prev => prev.map(user => 
          user.id === userId ? { ...user, is_active: false } : user
        ))
        break
      case 'verify':
        setUsers(prev => prev.map(user => 
          user.id === userId ? { ...user, is_verified: true } : user
        ))
        break
      case 'delete':
        setUsers(prev => prev.filter(user => user.id !== userId))
        break
    }
  }

  const UserDetailsDialog = ({ user, open, onOpenChange }) => {
    if (!user) return null
    
    const RoleIcon = getRoleIcon(user.role)
    
    return (
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center space-x-2 rtl:space-x-reverse">
              <RoleIcon className="w-5 h-5" />
              <span>تفاصيل المستخدم</span>
            </DialogTitle>
            <DialogDescription>
              معلومات تفصيلية عن {user.full_name}
            </DialogDescription>
          </DialogHeader>
          
          <Tabs defaultValue="info" className="w-full">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="info">المعلومات الأساسية</TabsTrigger>
              <TabsTrigger value="activity">النشاط</TabsTrigger>
              <TabsTrigger value="stats">الإحصائيات</TabsTrigger>
            </TabsList>
            
            <TabsContent value="info" className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">الاسم الكامل</label>
                  <p className="text-lg font-semibold">{user.full_name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">اسم المستخدم</label>
                  <p className="text-lg font-semibold">{user.username}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">البريد الإلكتروني</label>
                  <p className="text-lg font-semibold">{user.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">رقم الهاتف</label>
                  <p className="text-lg font-semibold">{user.phone}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">الدور</label>
                  <div className="mt-1">{getRoleBadge(user.role)}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">الحالة</label>
                  <div className="mt-1">{getStatusBadge(user)}</div>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="activity" className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">تاريخ التسجيل</label>
                  <p className="text-lg font-semibold">{new Date(user.created_at).toLocaleDateString('ar-SA')}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-600 dark:text-gray-400">آخر تسجيل دخول</label>
                  <p className="text-lg font-semibold">{new Date(user.last_login).toLocaleDateString('ar-SA')}</p>
                </div>
              </div>
            </TabsContent>
            
            <TabsContent value="stats" className="space-y-4">
              {user.role === 'merchant' ? (
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">{user.total_items}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">إجمالي السلع</p>
                  </div>
                  <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <p className="text-2xl font-bold text-green-600 dark:text-green-400">{user.total_auctions}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">إجمالي المزادات</p>
                  </div>
                  <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                    <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">{user.total_earnings} د.ك</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">إجمالي الأرباح</p>
                  </div>
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">{user.total_bids}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">إجمالي المزايدات</p>
                  </div>
                  <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <p className="text-2xl font-bold text-green-600 dark:text-green-400">{user.won_auctions}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">المزادات المكسوبة</p>
                  </div>
                </div>
              )}
            </TabsContent>
          </Tabs>
        </DialogContent>
      </Dialog>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">إدارة المستخدمين</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            إدارة التجار والمزايدين على المنصة
          </p>
        </div>
        <Button onClick={() => setShowAddUserDialog(true)}>
          <UserPlus className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
          إضافة مستخدم جديد
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">إجمالي المستخدمين</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{users.length}</p>
              </div>
              <Users className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">التجار</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {users.filter(u => u.role === 'merchant').length}
                </p>
              </div>
              <Store className="w-8 h-8 text-green-600 dark:text-green-400" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">المزايدين</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {users.filter(u => u.role === 'bidder').length}
                </p>
              </div>
              <GavelIcon className="w-8 h-8 text-purple-600 dark:text-purple-400" />
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">المستخدمون النشطون</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">
                  {users.filter(u => u.is_active).length}
                </p>
              </div>
              <CheckCircle className="w-8 h-8 text-orange-600 dark:text-orange-400" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 rtl:left-auto rtl:right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  placeholder="البحث عن المستخدمين..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 rtl:pl-4 rtl:pr-10"
                />
              </div>
            </div>
            
            <Select value={roleFilter} onValueChange={setRoleFilter}>
              <SelectTrigger className="w-full md:w-[180px]">
                <SelectValue placeholder="تصفية حسب الدور" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الأدوار</SelectItem>
                <SelectItem value="merchant">التجار</SelectItem>
                <SelectItem value="bidder">المزايدين</SelectItem>
                <SelectItem value="admin">المديرين</SelectItem>
              </SelectContent>
            </Select>
            
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-full md:w-[180px]">
                <SelectValue placeholder="تصفية حسب الحالة" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">جميع الحالات</SelectItem>
                <SelectItem value="active">نشط</SelectItem>
                <SelectItem value="inactive">معطل</SelectItem>
                <SelectItem value="verified">مؤكد</SelectItem>
                <SelectItem value="unverified">غير مؤكد</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Users Table */}
      <Card>
        <CardHeader>
          <CardTitle>قائمة المستخدمين</CardTitle>
          <CardDescription>
            عرض {filteredUsers.length} من أصل {users.length} مستخدم
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>المستخدم</TableHead>
                <TableHead>الدور</TableHead>
                <TableHead>الحالة</TableHead>
                <TableHead>تاريخ التسجيل</TableHead>
                <TableHead>آخر نشاط</TableHead>
                <TableHead>الإجراءات</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <AnimatePresence>
                {filteredUsers.map((user, index) => {
                  const RoleIcon = getRoleIcon(user.role)
                  return (
                    <motion.tr
                      key={user.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ delay: index * 0.05 }}
                      className="hover:bg-gray-50 dark:hover:bg-gray-800"
                    >
                      <TableCell>
                        <div className="flex items-center space-x-3 rtl:space-x-reverse">
                          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                            <RoleIcon className="w-5 h-5 text-white" />
                          </div>
                          <div>
                            <div className="font-medium text-gray-900 dark:text-white">
                              {user.full_name}
                            </div>
                            <div className="text-sm text-gray-500 dark:text-gray-400">
                              {user.email}
                            </div>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>{getRoleBadge(user.role)}</TableCell>
                      <TableCell>{getStatusBadge(user)}</TableCell>
                      <TableCell>
                        <div className="text-sm">
                          {new Date(user.created_at).toLocaleDateString('ar-SA')}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm">
                          {new Date(user.last_login).toLocaleDateString('ar-SA')}
                        </div>
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreHorizontal className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem 
                              onClick={() => {
                                setSelectedUser(user)
                                setShowUserDialog(true)
                              }}
                            >
                              <Eye className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                              عرض التفاصيل
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Edit className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                              تعديل
                            </DropdownMenuItem>
                            {user.is_active ? (
                              <DropdownMenuItem 
                                onClick={() => handleUserAction('deactivate', user.id)}
                                className="text-orange-600"
                              >
                                <Ban className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                                تعطيل
                              </DropdownMenuItem>
                            ) : (
                              <DropdownMenuItem 
                                onClick={() => handleUserAction('activate', user.id)}
                                className="text-green-600"
                              >
                                <CheckCircle className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                                تفعيل
                              </DropdownMenuItem>
                            )}
                            <DropdownMenuSeparator />
                            <DropdownMenuItem 
                              onClick={() => handleUserAction('delete', user.id)}
                              className="text-red-600"
                            >
                              <Trash2 className="w-4 h-4 mr-2 rtl:mr-0 rtl:ml-2" />
                              حذف
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </motion.tr>
                  )
                })}
              </AnimatePresence>
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* User Details Dialog */}
      <UserDetailsDialog 
        user={selectedUser}
        open={showUserDialog}
        onOpenChange={setShowUserDialog}
      />
    </div>
  )
}

export default UsersManagement
