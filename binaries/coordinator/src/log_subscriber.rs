use dora_core::coordinator_messages::LogMessage;
use eyre::{Context, ContextCompat};

use crate::tcp_utils::tcp_send;

pub struct LogSubscriber {
    pub level: log::LevelFilter,
    connection: Option<tokio::net::TcpStream>,
}

impl LogSubscriber {
    pub fn new(level: log::LevelFilter, connection: tokio::net::TcpStream) -> Self {
        Self {
            level,
            connection: Some(connection),
        }
    }

    pub async fn send_message(&mut self, message: &LogMessage) -> eyre::Result<()> {
        if message.level > self.level {
            return Ok(());
        }
        let message = serde_json::to_vec(&message)?;
        let connection = self.connection.as_mut().context("connection is closed")?;
        tcp_send(connection, &message)
            .await
            .context("failed to send message")?;
        Ok(())
    }

    pub fn is_closed(&self) -> bool {
        self.connection.is_none()
    }

    pub fn close(&mut self) {
        self.connection = None;
    }
}
