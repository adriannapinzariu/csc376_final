import java.io.*;
import java.net.*;

public class ChatClient {
    public static void main(String[] args) {
        if (args.length != 4) {
            System.out.println("Usage: java ChatClient -l <client listening port> -p <server port>");
            return;
        }

        int clientPort = Integer.parseInt(args[1]);
        int serverPort = Integer.parseInt(args[3]);

        try {
            Socket socket = new Socket("localhost", serverPort);
            ServerSocket serverSocket = new ServerSocket(clientPort);
            DataOutputStream output = new DataOutputStream(socket.getOutputStream());
            DataInputStream input = new DataInputStream(socket.getInputStream());
            BufferedReader consoleReader = new BufferedReader(new InputStreamReader(System.in));

            //Set username using first message
            System.out.print("Enter your username: ");
            String userName = consoleReader.readLine();
            output.writeUTF(userName);

            //Thread for receiving messages
            Thread receiveThread = new Thread(() -> {
                try {
                    String messageReceived;
                    while ((messageReceived = input.readUTF()) != null) {
                        System.out.println(messageReceived);
                    }
                } catch (IOException e) {
                    System.err.println(e.getMessage());
                }
            });

            //Thread for receiving files
            Thread receiveFileThread = new Thread(() -> {
                try {
                    while (true) {
                        Socket fileSocket = serverSocket.accept();
                        DataInputStream file_input = new DataInputStream(fileSocket.getInputStream());
                        String file = file_input.readUTF();
                        FileOutputStream fileOut = new FileOutputStream(file);
                        byte[] buffer = new byte[1500];
                        int number_read;
                        while ((number_read = file_input.read(buffer)) != -1) {
                            fileOut.write(buffer, 0, number_read);
                        }
                        fileSocket.close();
                    }
                } catch (IOException e) {
                    System.err.println(e.getMessage());
                }
            });

            receiveThread.start();
            receiveFileThread.start();

            //Sending messages
            while (true) {
                System.out.println("Enter an option ('m', 'f', 'x'):");
                System.out.println("  (M)essage (send)");
                System.out.println("  (F)ile (request)");
                System.out.println("  e(X)it");
                String option = consoleReader.readLine();
                if (option.equals("m")) {
                    System.out.println("Enter your message:");
                    String message = consoleReader.readLine();
                    output.writeUTF("m:" + message);
                } else if (option.equals("f")) {
                    System.out.println("Who owns the file?");
                    String fileOwner = consoleReader.readLine();
                    System.out.println("Which file do you want?");
                    String fileName = consoleReader.readLine();
                    output.writeUTF("f:" + fileOwner + ":" + fileName);
                } else if (option.equals("x")) {
                    System.out.println("closing your sockets... goodbye");
                    output.writeUTF("x");
                    socket.close();
                    serverSocket.close();
                    break;
                }
            }
            receiveThread.join();
        } catch (IOException | InterruptedException e) {
            System.err.println(e.getMessage());
        }
    }
}

