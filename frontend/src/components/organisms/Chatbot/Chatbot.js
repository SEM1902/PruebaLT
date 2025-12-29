import React, { useState, useRef, useEffect } from 'react';
import { Card, Button as BootstrapButton } from 'react-bootstrap';
import { FaRobot, FaTimes, FaPaperPlane, FaSpinner } from 'react-icons/fa';
import api from '../../../services/api';
import Button from '../../atoms/Button/Button';
import Spinner from '../../atoms/Spinner/Spinner';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '¡Hola! Soy tu asistente virtual. Puedo ayudarte con información sobre empresas, productos, inventario, cantidades, valores en USD/EUR/COP, y más. ¿En qué puedo ayudarte?'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || loading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Agregar mensaje del usuario
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await api.post('/api/chatbot/', {
        question: userMessage
      });

      // Agregar respuesta del asistente
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.response
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: error.response?.data?.error || 'Lo siento, ocurrió un error al procesar tu pregunta. Por favor, intenta nuevamente.'
      }]);
    } finally {
      setLoading(false);
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  return (
    <>
      {/* Botón flotante para abrir el chatbot */}
      {!isOpen && (
        <button
          className="chatbot-toggle-btn"
          onClick={() => setIsOpen(true)}
          aria-label="Abrir chatbot"
        >
          <FaRobot size={24} />
        </button>
      )}

      {/* Panel del chatbot */}
      {isOpen && (
        <div className="chatbot-container">
          <Card className="chatbot-card">
            <Card.Header className="chatbot-header">
              <div className="d-flex align-items-center gap-2">
                <FaRobot />
                <strong>Asistente Virtual</strong>
              </div>
              <Button
                variant="link"
                size="small"
                onClick={() => setIsOpen(false)}
                className="chatbot-close-btn"
                aria-label="Cerrar chatbot"
              >
                <FaTimes />
              </Button>
            </Card.Header>
            <Card.Body className="chatbot-body">
              <div className="chatbot-messages">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`chatbot-message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
                  >
                    <div className="message-content">
                      {message.content}
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="chatbot-message assistant-message">
                    <div className="message-content d-flex align-items-center gap-2">
                      <Spinner size="small" />
                      <span>Pensando...</span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            </Card.Body>
            <Card.Footer className="chatbot-footer">
              <form onSubmit={handleSendMessage} className="chatbot-form">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Escribe tu pregunta..."
                  className="chatbot-input"
                  disabled={loading}
                />
                <Button
                  type="submit"
                  variant="primary"
                  size="small"
                  disabled={!inputMessage.trim() || loading}
                  className="chatbot-send-btn"
                >
                  {loading ? (
                    <FaSpinner className="spinning" />
                  ) : (
                    <FaPaperPlane />
                  )}
                </Button>
              </form>
            </Card.Footer>
          </Card>
        </div>
      )}
    </>
  );
};

export default Chatbot;

