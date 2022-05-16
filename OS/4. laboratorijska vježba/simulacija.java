package prvi;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

public class simulacija {
	
	static int vrijeme;
	
	private enum TipRasporeda{
		SCHED_FIFO,
		SCHED_PR
	}
	
	private static class Dretva{
			
		private int id;
		private int vrijemeDolaska;
		private int trajanje;
		private int prioritet;
		private TipRasporeda raspored;
		
		public Dretva(int id, int vrijemeDolaska, int trajanje, int prioritet, TipRasporeda raspored) {
			super();
			this.id = id;
			this.vrijemeDolaska = vrijemeDolaska;
			this.trajanje = trajanje;
			this.prioritet = prioritet;
			this.raspored = raspored;
		}

		@Override
		public int hashCode() {
			final int prime = 31;
			int result = 1;
			result = prime * result + vrijemeDolaska;
			result = prime * result + trajanje;
			result = prime * result + id;
			result = prime * result + prioritet;
			result = prime * result + ((raspored == null) ? 0 : raspored.hashCode());
			return result;
		}
		
		@Override
		public String toString(){
			return (id + "/" + prioritet + "/" + trajanje);
		}

		@Override
		public boolean equals(Object obj) {
			if (this == obj)
				return true;
			if (obj == null)
				return false;
			if (!(obj instanceof Dretva))
				return false;
			Dretva other = (Dretva) obj;
			if (vrijemeDolaska != other.vrijemeDolaska)
				return false;
			if (trajanje != other.trajanje)
				return false;
			if (id != other.id)
				return false;
			if (prioritet != other.prioritet)
				return false;
			if (raspored != other.raspored)
				return false;
			return true;
		}
		
		
		public int getId(){
			return id;
		}
		
		public int getVrijemeDolaska(){
			return vrijemeDolaska;
		}
		
		public void setTrajanje(int duration){
			this.trajanje = duration;
		}
		
		public int getPrioritet(){
			return prioritet;
		}	
		
		public int getTrajanje(){
			return trajanje;
		}	
	}
	
	private static class Rasporedivac{
		
		protected List<Dretva> redCekanja;
		
		public Rasporedivac(){
			redCekanja = new LinkedList<>();
			System.out.println("  t   AKT    PR1    PR2    PR3    PR4");
		}
		
		public void ispisi_stanje(){
			System.out.printf("%3d ",simulacija.vrijeme);
			
			Iterator<Dretva> it = redCekanja.iterator();
			
			for(int i = 0; i < 5; i++){
				if(it.hasNext()){
					System.out.print("  " + it.next().toString());
				}else{
					System.out.printf(" -/-/- ");
				}
			}
			System.out.println();
		}
		
		public void napomena(){
			System.out.println("Raspored prve dvije dretve je PR, druge dvije FIFO te zadnje"
					+ "dvije takoder PR");
			System.out.println("Vremena dolaska su redom: 1, 3, 7, 12, 20");
		}
		
		public void dodajRedCekanja(Dretva dretva){
			ispisi_stanje();
			redCekanja.add(dretva);
			System.out.printf("%3d",simulacija.vrijeme);
			System.out.println(" -- nova dretva id=" + dretva.getId() + ", p=" + dretva.getTrajanje() + ", prio=" + 
					dretva.getPrioritet());
		}
		
		public void rasporedi(){
			redCekanja.sort((d1,d2) -> {
				if(d1.getPrioritet() > d2.getPrioritet())
					return -1;
				if(d1.getPrioritet() < d2.getPrioritet())
					return 1;
				if(d1.getPrioritet() == d2.getPrioritet()){
					if(d1.getVrijemeDolaska() < d2.getVrijemeDolaska())
						return -1;
					else
						return 1;
				}
				return 0;
			});
			
			ispisi_stanje();
			
			if(!redCekanja.isEmpty()){
				Dretva aktivna = redCekanja.get(0);
				if(aktivna.getTrajanje() > 1){
					aktivna.setTrajanje(aktivna.getTrajanje() -1);
				}else{
					System.out.println("Dretva " + aktivna.getId() + " zavrsila");
					redCekanja.remove(0);
				}
			}
		}	
	}
	
	public static void main(String[] args) {
		
		System.out.println("Prioritetno rasporedivanje");
		
		Rasporedivac scheduler = new Rasporedivac();
		
		Dretva[] dretve ={
				new Dretva(3, 1, 5, 3, TipRasporeda.SCHED_PR),
				new Dretva(5, 3, 6, 5, TipRasporeda.SCHED_PR),
				new Dretva(2, 7, 3, 5, TipRasporeda.SCHED_FIFO),
				new Dretva(1, 12, 5, 3, TipRasporeda.SCHED_FIFO),
				new Dretva(6, 20, 3, 6, TipRasporeda.SCHED_PR),
				new Dretva(7, 20, 4, 7, TipRasporeda.SCHED_PR)
		};
		
		for(; vrijeme < 30; vrijeme++){
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			
			for(Dretva dretva : dretve){
				if(dretva.getVrijemeDolaska() == vrijeme){
					scheduler.dodajRedCekanja(dretva);
				}
			}
			scheduler.rasporedi();
		}
	}
	
}
