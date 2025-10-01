import React from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  LayoutDashboard, 
  Users, 
  Gavel, 
  Package, 
  BarChart3, 
  Settings, 
  ChevronLeft,
  Shield,
  TrendingUp,
  Activity
} from 'lucide-react'
import { cn } from '@/lib/utils'

const Sidebar = ({ isOpen, onToggle }) => {
  const location = useLocation()

  const menuItems = [
    {
      title: 'لوحة التحكم',
      icon: LayoutDashboard,
      path: '/',
      description: 'نظرة عامة على النظام'
    },
    {
      title: 'إدارة المستخدمين',
      icon: Users,
      path: '/users',
      description: 'التجار والمزايدين'
    },
    {
      title: 'إدارة المزادات',
      icon: Gavel,
      path: '/auctions',
      description: 'المزادات النشطة والمنتهية'
    },
    {
      title: 'إدارة السلع',
      icon: Package,
      path: '/items',
      description: 'مراجعة وإدارة السلع'
    },
    {
      title: 'التحليلات',
      icon: BarChart3,
      path: '/analytics',
      description: 'تقارير وإحصائيات'
    },
    {
      title: 'الإعدادات',
      icon: Settings,
      path: '/settings',
      description: 'إعدادات النظام'
    }
  ]

  const sidebarVariants = {
    open: {
      width: '280px',
      transition: {
        duration: 0.3,
        ease: 'easeInOut'
      }
    },
    closed: {
      width: '80px',
      transition: {
        duration: 0.3,
        ease: 'easeInOut'
      }
    }
  }

  const contentVariants = {
    open: {
      opacity: 1,
      x: 0,
      transition: {
        delay: 0.1,
        duration: 0.2
      }
    },
    closed: {
      opacity: 0,
      x: -20,
      transition: {
        duration: 0.2
      }
    }
  }

  return (
    <motion.aside
      variants={sidebarVariants}
      animate={isOpen ? 'open' : 'closed'}
      className="bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col shadow-lg"
    >
      {/* Header */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <AnimatePresence>
            {isOpen && (
              <motion.div
                variants={contentVariants}
                initial="closed"
                animate="open"
                exit="closed"
                className="flex items-center space-x-3 rtl:space-x-reverse"
              >
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Shield className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900 dark:text-white">BidFlow</h1>
                  <p className="text-xs text-gray-500 dark:text-gray-400">لوحة الإدارة</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          
          <button
            onClick={onToggle}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <motion.div
              animate={{ rotate: isOpen ? 0 : 180 }}
              transition={{ duration: 0.3 }}
            >
              <ChevronLeft className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            </motion.div>
          </button>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item, index) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          
          return (
            <motion.div
              key={item.path}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  cn(
                    'flex items-center p-3 rounded-lg transition-all duration-200 group relative',
                    isActive
                      ? 'bg-primary text-primary-foreground shadow-md'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-primary'
                  )
                }
              >
                <Icon className={cn(
                  'w-5 h-5 flex-shrink-0',
                  isActive ? 'text-primary-foreground' : 'text-gray-500 dark:text-gray-400 group-hover:text-primary'
                )} />
                
                <AnimatePresence>
                  {isOpen && (
                    <motion.div
                      variants={contentVariants}
                      initial="closed"
                      animate="open"
                      exit="closed"
                      className="ml-3 rtl:ml-0 rtl:mr-3"
                    >
                      <div className="font-medium">{item.title}</div>
                      <div className={cn(
                        'text-xs opacity-75',
                        isActive ? 'text-primary-foreground' : 'text-gray-500 dark:text-gray-400'
                      )}>
                        {item.description}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Active indicator */}
                {isActive && (
                  <motion.div
                    layoutId="activeIndicator"
                    className="absolute right-0 top-1/2 transform -translate-y-1/2 w-1 h-8 bg-primary-foreground rounded-l-full"
                  />
                )}
              </NavLink>
            </motion.div>
          )
        })}
      </nav>

      {/* Footer Stats */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <AnimatePresence>
          {isOpen ? (
            <motion.div
              variants={contentVariants}
              initial="closed"
              animate="open"
              exit="closed"
              className="space-y-3"
            >
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">حالة النظام</span>
                <div className="flex items-center space-x-1 rtl:space-x-reverse">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-green-600 dark:text-green-400 text-xs">نشط</span>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="bg-gray-50 dark:bg-gray-700 p-2 rounded">
                  <div className="flex items-center space-x-1 rtl:space-x-reverse">
                    <TrendingUp className="w-3 h-3 text-blue-500" />
                    <span className="text-gray-600 dark:text-gray-400">المبيعات</span>
                  </div>
                  <div className="font-semibold text-gray-900 dark:text-white">+12%</div>
                </div>
                
                <div className="bg-gray-50 dark:bg-gray-700 p-2 rounded">
                  <div className="flex items-center space-x-1 rtl:space-x-reverse">
                    <Activity className="w-3 h-3 text-green-500" />
                    <span className="text-gray-600 dark:text-gray-400">النشاط</span>
                  </div>
                  <div className="font-semibold text-gray-900 dark:text-white">عالي</div>
                </div>
              </div>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-center"
            >
              <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-lg flex items-center justify-center">
                <Activity className="w-4 h-4 text-white" />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.aside>
  )
}

export default Sidebar
