-- ============================================================================
-- Script de Criação do Banco de Dados (PostgreSQL)
-- Projeto: Sistema Web de Gestão de Relacionamento e Automação de Marketing
--          com Inteligência Artificial para Confeitarias (Delícias da Eli)
-- Autor: Marten Alexandre da Rosa
-- ============================================================================

-- Tabela de Clientes
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_clients_id ON clients (id);
CREATE INDEX IF NOT EXISTS ix_clients_email ON clients (email);

-- Tabela de Eventos e Datas Comemorativas
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    advance_days INTEGER DEFAULT 7,
    custom_message TEXT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- Valores: 'pending', 'approved', 'sent'
    client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_events_id ON events (id);
CREATE INDEX IF NOT EXISTS ix_events_client_id ON events (client_id);

-- ============================================================================
-- Dados Iniciais (Seed) para Demonstração e Testes
-- ============================================================================
INSERT INTO clients (name, email, phone)
VALUES ('Cliente Demonstração', 'cliente.teste@exemplo.com', '5551999999999')
ON CONFLICT (email) DO NOTHING;

INSERT INTO events (title, event_date, advance_days, custom_message, status, client_id)
SELECT 
    'Aniversário',
    CURRENT_DATE + INTERVAL '7 days',
    7,
    'Olá Cliente Demonstração! Falta apenas 1 semana para o seu Aniversário. Que tal encomendar um bolo especial na Delícias da Eli?',
    'pending',
    id
FROM clients
WHERE email = 'cliente.teste@exemplo.com'
LIMIT 1;