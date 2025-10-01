import React, { createContext, useContext, useEffect, useState, useRef } from 'react'
import { useAuth } from './AuthContext'

const SocketContext = createContext()

export const useSocket = () => {
  const context = useContext(SocketContext)
  if (!context) {
    throw new Error('useSocket must be used within a SocketProvider')
  }
  return context
}

export const SocketProvider = ({ children }) => {
  const { user, token } = useAuth()
  const [socket, setSocket] = useState(null)
  const [isConnected, setIsConnected] = useState(false)
  const [liveAuctions, setLiveAuctions] = useState({})
  const [notifications, setNotifications] = useState([])
  const reconnectTimeoutRef = useRef(null)
  const reconnectAttemptsRef = useRef(0)
  const maxReconnectAttempts = 5

  const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'ws://localhost:5000'

  useEffect(() => {
    if (user && token) {
      connectSocket()
    } else {
      disconnectSocket()
    }

    return () => {
      disconnectSocket()
    }
  }, [user, token])

  const connectSocket = () => {
    try {
      const ws = new WebSocket(`${SOCKET_URL}/ws?token=${token}`)
      
      ws.onopen = () => {
        console.log('WebSocket connected')
        setIsConnected(true)
        setSocket(ws)
        reconnectAttemptsRef.current = 0
        
        // Send authentication
        ws.send(JSON.stringify({
          type: 'auth',
          token: token
        }))
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          handleSocketMessage(data)
        } catch (error) {
          console.error('Error parsing socket message:', error)
        }
      }

      ws.onclose = (event) => {
        console.log('WebSocket disconnected:', event.code, event.reason)
        setIsConnected(false)
        setSocket(null)
        
        // Attempt to reconnect if not intentionally closed
        if (event.code !== 1000 && reconnectAttemptsRef.current < maxReconnectAttempts) {
          scheduleReconnect()
        }
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setIsConnected(false)
      }

    } catch (error) {
      console.error('Error creating WebSocket connection:', error)
      scheduleReconnect()
    }
  }

  const disconnectSocket = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }
    
    if (socket) {
      socket.close(1000, 'User disconnected')
      setSocket(null)
    }
    
    setIsConnected(false)
  }

  const scheduleReconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
    }
    
    const delay = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000)
    reconnectAttemptsRef.current += 1
    
    console.log(`Scheduling reconnect attempt ${reconnectAttemptsRef.current} in ${delay}ms`)
    
    reconnectTimeoutRef.current = setTimeout(() => {
      if (user && token) {
        connectSocket()
      }
    }, delay)
  }

  const handleSocketMessage = (data) => {
    switch (data.type) {
      case 'auction_update':
        handleAuctionUpdate(data.payload)
        break
      
      case 'new_bid':
        handleNewBid(data.payload)
        break
      
      case 'auction_ended':
        handleAuctionEnded(data.payload)
        break
      
      case 'notification':
        handleNotification(data.payload)
        break
      
      case 'bid_confirmation':
        handleBidConfirmation(data.payload)
        break
      
      case 'outbid_notification':
        handleOutbidNotification(data.payload)
        break
      
      default:
        console.log('Unknown socket message type:', data.type)
    }
  }

  const handleAuctionUpdate = (auction) => {
    setLiveAuctions(prev => ({
      ...prev,
      [auction.id]: {
        ...prev[auction.id],
        ...auction,
        lastUpdate: Date.now()
      }
    }))
  }

  const handleNewBid = (bidData) => {
    const { auction_id, amount, bidder_name, timestamp } = bidData
    
    setLiveAuctions(prev => ({
      ...prev,
      [auction_id]: {
        ...prev[auction_id],
        current_price: amount,
        total_bids: (prev[auction_id]?.total_bids || 0) + 1,
        last_bidder: bidder_name,
        last_bid_time: timestamp,
        lastUpdate: Date.now()
      }
    }))

    // Add notification if user was previously the highest bidder
    if (prev[auction_id]?.last_bidder === user?.username && bidder_name !== user?.username) {
      addNotification({
        type: 'outbid',
        title: 'تم تجاوز مزايدتك',
        message: `تم تجاوز مزايدتك في المزاد "${prev[auction_id]?.title}"`,
        auction_id: auction_id,
        timestamp: Date.now()
      })
    }
  }

  const handleAuctionEnded = (auctionData) => {
    const { auction_id, winner_id, final_price } = auctionData
    
    setLiveAuctions(prev => ({
      ...prev,
      [auction_id]: {
        ...prev[auction_id],
        status: 'ended',
        final_price: final_price,
        winner_id: winner_id,
        lastUpdate: Date.now()
      }
    }))

    // Notify if user won or lost
    if (winner_id === user?.id) {
      addNotification({
        type: 'auction_won',
        title: 'مبروك! لقد ربحت المزاد',
        message: `لقد ربحت المزاد "${prev[auction_id]?.title}" بمبلغ ${final_price} د.ك`,
        auction_id: auction_id,
        timestamp: Date.now()
      })
    }
  }

  const handleNotification = (notification) => {
    addNotification(notification)
  }

  const handleBidConfirmation = (bidData) => {
    const { auction_id, amount, success, message } = bidData
    
    if (success) {
      addNotification({
        type: 'bid_success',
        title: 'تم وضع مزايدتك بنجاح',
        message: `تم وضع مزايدة بقيمة ${amount} د.ك`,
        auction_id: auction_id,
        timestamp: Date.now()
      })
    } else {
      addNotification({
        type: 'bid_error',
        title: 'فشل في وضع المزايدة',
        message: message || 'حدث خطأ أثناء وضع المزايدة',
        auction_id: auction_id,
        timestamp: Date.now()
      })
    }
  }

  const handleOutbidNotification = (data) => {
    addNotification({
      type: 'outbid',
      title: 'تم تجاوز مزايدتك',
      message: `تم تجاوز مزايدتك في المزاد "${data.auction_title}"`,
      auction_id: data.auction_id,
      timestamp: Date.now()
    })
  }

  const addNotification = (notification) => {
    setNotifications(prev => [
      {
        id: Date.now() + Math.random(),
        ...notification,
        read: false
      },
      ...prev.slice(0, 49) // Keep only last 50 notifications
    ])
  }

  const placeBid = (auctionId, amount) => {
    if (socket && isConnected) {
      socket.send(JSON.stringify({
        type: 'place_bid',
        payload: {
          auction_id: auctionId,
          amount: amount
        }
      }))
      return true
    }
    return false
  }

  const joinAuction = (auctionId) => {
    if (socket && isConnected) {
      socket.send(JSON.stringify({
        type: 'join_auction',
        payload: {
          auction_id: auctionId
        }
      }))
    }
  }

  const leaveAuction = (auctionId) => {
    if (socket && isConnected) {
      socket.send(JSON.stringify({
        type: 'leave_auction',
        payload: {
          auction_id: auctionId
        }
      }))
    }
  }

  const markNotificationAsRead = (notificationId) => {
    setNotifications(prev => 
      prev.map(notif => 
        notif.id === notificationId 
          ? { ...notif, read: true }
          : notif
      )
    )
  }

  const clearAllNotifications = () => {
    setNotifications([])
  }

  const getAuctionData = (auctionId) => {
    return liveAuctions[auctionId] || null
  }

  const value = {
    socket,
    isConnected,
    liveAuctions,
    notifications,
    placeBid,
    joinAuction,
    leaveAuction,
    getAuctionData,
    markNotificationAsRead,
    clearAllNotifications,
    unreadNotifications: notifications.filter(n => !n.read).length
  }

  return (
    <SocketContext.Provider value={value}>
      {children}
    </SocketContext.Provider>
  )
}
