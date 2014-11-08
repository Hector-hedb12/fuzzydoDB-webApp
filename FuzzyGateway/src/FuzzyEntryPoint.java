import fuzzy.database.Connector;
import java.sql.SQLException;
import py4j.GatewayServer;

public class FuzzyEntryPoint {

    private Connector connector;

    public FuzzyEntryPoint() throws SQLException {
      connector = new Connector("127.0.0.1", "fuzzy", "fuzzy", "fuzzy");
      connector.setLibraryMode(true);
    }

    public Connector getConnector() {
        return connector;
    }

    public static void main(String[] args) throws SQLException {
        GatewayServer gatewayServer = new GatewayServer(new FuzzyEntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }

}