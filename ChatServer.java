import java.io.*;
import java.net.*;
import java.util.concurrent.ConcurrentHashMap;

public class ChatServer {
    private static final ConcurrentHashMap<String, Client> clients = new ConcurrentHashMap<>();

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Usage: java ChatServer <port number>");
            return;
        }

        int port = Integer.parseInt(args[0]);

        try {
            ServerSocket serverSocket = new ServerSocket(port);
            while (true) {
                Socket socket = serverSocket.accept();
                new Thread(new Client(socket)).start();
            }
        } catch (IOException e) {
            System.err.println(e.getMessage());
        }
    }
    
    private static class Client extends Thread {
        private final Socket socket;
        private String clientUsername;
        private int filePort;
        private DataOutputStream output;

        public Client(Socket socket) {
            this.socket = socket;
        }

        @Override
        public void run() {
            try {
                DataInputStream input = new DataInputStream(socket.getInputStream());
                output = new DataOutputStream(socket.getOutputStream());

                // Get the username from the first message
                clientUsername = input.readUTF();
                clients.put(clientUsername, this);

                String message;
                while ((message = input.readUTF()) != null) {
                    if (message.startsWith("m:")) {
                        String clientMessage = clientUsername + ": " + message.substring(2);
                        sendMessage(clientMessage, this);
                    } else if (message.startsWith("f:")) {
                        String[] parts = message.split(":");
                        if (parts.length == 3) {
                            String fileOwner = parts[1];
                            String fileName = parts[2];
                            handleFileRequest(fileOwner, fileName);
                        }
                    } else if (message.equals("x")) {
                        break;
                    }
                }
            } catch (IOException e) {
                System.err.println(e.getMessage());
            } finally {
                disconnect();
            }
        }

        private void sendMessage(String message, Client originalClient) {
            for (Client client: clients.values()) {
                if (client != originalClient) {
                    try {
                        client.output.writeUTF(message);
                    } catch (IOException e) {
                        System.err.println(e.getMessage());
                    }
                }
            }
        }

        private void handleFileRequest(String owner, String fileName) {
            Client ownerClient = clients.get(owner);
            if (ownerClient != null) {
                try {
                    ownerClient.output.writeUTF("f:" + clientUsername + ":" + fileName);
                } catch (IOException e) {
                    System.err.println(e.getMessage());
                }
            }
        }

        private void disconnect() {
            try {
                clients.remove(clientUsername);
                socket.close();
            } catch (IOException e) {
                System.err.println(e.getMessage());
            }
        }
    }
}

