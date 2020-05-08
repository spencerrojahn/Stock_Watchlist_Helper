import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.*;

public class TickerScraper {

	public static void main(String[] args) throws IOException {
		
		FileWriter writer = new FileWriter("TradingAutomation/tickers.txt");
		int tickerNum = 1;
		
		while(true) {
			
			final String url = getURL(tickerNum);
			
			try {
				
				final Document doc = Jsoup.connect(url).get();
				Elements tickers = doc.select("a.screener-link-primary");
				for (Element ticker: tickers) {
					writer.write(ticker.text() + "\n");
					tickerNum+=1;
				}
				
				if (tickerNum % 20 != 1) {
					break;
				}
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		writer.close();

	}
	
//  NASDAQ, PRICE<1, CURRENT_VOLUME>1M
//	https://finviz.com/screener.ashx?v=111&f=exch_nasd,sh_curvol_o1000,sh_price_u1&o=price
//	https://finviz.com/screener.ashx?v=111&f=exch_nasd,sh_curvol_o1000,sh_price_u1&o=price&r=21
//	https://finviz.com/screener.ashx?v=111&f=exch_nasd,sh_curvol_o1000,sh_price_u1&o=price&r=41
	
//  NASDAQ, PRICE<1, AVERAGE_VOLUME>1M <-----
//  https://finviz.com/screener.ashx?v=111&f=exch_nasd,sh_avgvol_o1000,sh_price_u1&o=price
	
//  NYSE, PRICE<1, AVERAGE_VOLUME>1M
//  https://finviz.com/screener.ashx?v=111&f=exch_nyse,sh_avgvol_o1000,sh_price_u1&o=price
	
//  NASDAQ, PRICE<2, AVERAGE_VOLUME>2M
//  https://finviz.com/screener.ashx?v=111&f=exch_nasd,sh_avgvol_o2000,sh_price_u2&o=price

	static String getURL(int i) {
		String url;
		if (i == 1) {
			url = "https://finviz.com/screener.ashx?v=111&f=exch_nasd,sh_avgvol_o1000,sh_price_u1&o=price";
		} else {
			url = "https://finviz.com/screener.ashx?v=111&f=exch_nasd,sh_avgvol_o1000,sh_price_u1&o=price&r=" + i;
		}
		return url;
	}
}
