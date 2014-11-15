import java.util.Map;
import constant.Region;
import dto.Summoner.Summoner;
import main.java.riotapi.RiotApi;
import com.google.gson.*;

public class Main {

    public static void main(String[] args) throws Exception {
        RiotApi api = new RiotApi("a2b74008-5372-42c3-8bc1-3b3b3e0d9b19");

        Map<String, Summoner> summoners = api.getSummonersByName(Region.NA, "vangod, tryndamere");
        Summoner summoner = summoners.get("vangod");
        long id = summoner.getId();
        System.out.println(id);
    }
}
