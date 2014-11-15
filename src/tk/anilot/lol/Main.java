package tk.anilot.lol;

import java.util.Map;
import java.util.Set;

import constant.Region;
import dto.Summoner.RunePage;
import dto.Summoner.RunePages;
import dto.Summoner.RuneSlot;
import dto.Summoner.Summoner;
import main.java.riotapi.RiotApi;
import com.google.gson.*;

public class Main {

    public static void main(String[] args) throws Exception {
        RiotApi api = new RiotApi("a2b74008-5372-42c3-8bc1-3b3b3e0d9b19");
        api.setRegion(Region.NA);

        Map<String, Summoner> summoners = api.getSummonersByName("vangod, sepcentum");
        Summoner summoner = summoners.get("vangod");
        long id = summoner.getId();
        System.out.println(id);

        Map<String, RunePages> runePagesMap =  api.getRunePages(id);
        RunePages runePages = runePagesMap.get(String.valueOf(id));
        Set<RunePage> runePageSet = runePages.getPages();
        for(RunePage i : runePageSet){
            System.out.println(i.getName());
        }

    }
}
