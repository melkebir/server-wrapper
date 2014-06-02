import java.io.OutputStream;
import java.net.Socket;
import java.io.IOException;

class TestClient 
{
	public static void main(String args[])
	{
		try
		{
			Socket socket = null;
			String host = "127.0.0.1";
			socket = new Socket(host, 9001);

			// send ping
			OutputStream out = socket.getOutputStream();
			out.write(0);

			// name_length = 0
			out.write(0);
			out.write(0);
			out.write(0);
			out.write(0);

			// payload_length = 0
			out.write(0);
			out.write(0);
			out.write(0);
			out.write(0);

			try {
				Thread.sleep(1000);
			} catch(InterruptedException ex) {
				Thread.currentThread().interrupt();
			}
			socket.close();
		}
		catch (Exception e)
		{
			System.err.println(e);
		}

		System.out.println("Hello World!");
	}
}
