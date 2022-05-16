package drugi;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
	 
	public class visekriterijsko {
	 
	    static int vrijeme;
	   
	    private enum TipRasporeda{
	        SCHED_FIFO, SCHED_RR
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
	        public String toString(){
	            return (id + "/" + prioritet + "/" + trajanje);
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
	       
	        public int getTrajanje(){
	            return trajanje;
	        }
	       
	        public void setTrajanje(int duration){
	            this.trajanje = duration;
	        }
	       
	        public int getPrioritet(){
	            return prioritet;
	        }  
	       
	        public TipRasporeda getSchedule(){
	            return raspored;
	        }
	    }
	   
	    private static class RasporedivacNapredni{
	       
	        protected List<Dretva> redCekanja;
	       
	        public RasporedivacNapredni(){
	            redCekanja = new LinkedList<>();
	            System.out.println("  t   AKT    PR1    PR2    PR3    PR4");
	        }
	       
	        public void dodajRedCekanja(Dretva dretva){
	            redCekanja.add(dretva);
	            System.out.printf("%3d", visekriterijsko.vrijeme);
	            System.out.println(" -- nova dretva id=" + dretva.getId() + ", p=" + dretva.getTrajanje() + ", prio=" + dretva.getPrioritet());
	            sortiraj();
	            ispisi_stanje();
	        }
	       
	        public void odvrtiTrenutak(){
	            smanjiPrvu();
	            roundRobbinCheck();
	            ispisi_stanje();
	        }
	       
	        public void sortiraj(){
	            if(redCekanja.size() > 1 ) {
	                redCekanja.sort((d1, d2) -> {
	                    if (d1.getPrioritet() > d2.getPrioritet()) {
	                        return -1;
	                    } else if (d1.getPrioritet() < d2.getPrioritet()) {
	                        return 1;
	                    }
	                    return 0;
	                });
	            }
	        }
	       
	        public void roundRobbinCheck(){
	            if(redCekanja.size() > 0 && redCekanja.get(0).getSchedule() == TipRasporeda.SCHED_RR){
	                Dretva first = redCekanja.get(0);
	                int firstDifferentPriority = 0;
	                for(firstDifferentPriority = 0; firstDifferentPriority < redCekanja.size(); ++firstDifferentPriority){
	                    if(redCekanja.get(firstDifferentPriority).getPrioritet() != first.getPrioritet()){
	                        break;
	                    }
	                }
	               
	                redCekanja.add(firstDifferentPriority, first);
	                redCekanja.remove(0);
	            }
	        }
	       
	        public void smanjiPrvu(){
	            if(!redCekanja.isEmpty()){
	                Dretva aktivna = redCekanja.get(0);
	                if (aktivna.getTrajanje() > 1) {
	                    aktivna.setTrajanje(aktivna.getTrajanje() - 1);
	                } else {
	                    System.out.println(" Dretva " + aktivna.getId() + " zavrsila");
	                    redCekanja.remove(0);
	                }
	            }
	        }
	       
	        public void ispisi_stanje(){
	            System.out.printf("%3d ",visekriterijsko.vrijeme);
	           
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
	    }
	   
	    public static void main(String[] args) {
	       
	        System.out.println("Visekriterijsko rasporedivanje");
	       
	        RasporedivacNapredni scheduler = new RasporedivacNapredni();
	       
	        Dretva[] dretve = {
	                new Dretva(3, 1, 5, 3, TipRasporeda.SCHED_RR),
	                new Dretva(5, 3, 6, 5, TipRasporeda.SCHED_RR),
	                new Dretva(2, 7, 3, 5, TipRasporeda.SCHED_FIFO),
	                new Dretva(1, 12, 5, 3, TipRasporeda.SCHED_FIFO),
	                new Dretva(6, 20, 3, 6, TipRasporeda.SCHED_RR),
	                new Dretva(7, 20, 4, 7, TipRasporeda.SCHED_RR),
	        };
	   
	        for(vrijeme = 0; vrijeme < 30; vrijeme++){
	            try {
	                Thread.sleep(1000);
	            } catch (InterruptedException e) {
	                e.printStackTrace();
	            }
	           
	            scheduler.odvrtiTrenutak();
	           
	            for (Dretva dretva : dretve) {
	                if (dretva.getVrijemeDolaska() == vrijeme) {
	                    scheduler.dodajRedCekanja(dretva);
	                }
	            }
	        }
	    }  
}
