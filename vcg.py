class Bidder:

  ## each bidder is modeled by a linear equation bid = intercept - slope * curr_holdings
  def __init__(self, name, start_intercept, end_intercept, max_demand):
    
    # initializing variables
    self.name = name
    self.start_intercept = start_intercept
    self.end_intercept = end_intercept
    self.max_demand = max_demand

    self.slope = (start_intercept-end_intercept)/max_demand

    # generated variables
    self.curr_holdings = 0
    self.total_payment = 0
    self.vcg_payment = 0

  def get_next_bid(self):
    return self.start_intercept - self.slope * (self.curr_holdings) if self.curr_holdings < self.max_demand else 0

  def receive_object(self):
    self.total_payment += self.get_next_bid()
    self.curr_holdings += 1
    return

  def set_vcg_payment(self, vcg_payment):
    self.vcg_payment = vcg_payment

class VCG_Auction: 

  def __init__(self, name, bidder_list, total_objects):

    # initializing variables
    self.name = name
    self.bidder_list = bidder_list
    self.total_objects = total_objects

  def clone_bidder(self, bidder):
    return Bidder(bidder.name, bidder.start_intercept, bidder.end_intercept, bidder.max_demand)

  def run_auction(self):

    # run the auction with all bidders
    main_auction = VCG_sub_auction(self.bidder_list, self.total_objects)
    main_auction.run_auction()

    total_social_good = main_auction.auction_revenue

    for bidder in self.bidder_list:
      # remove the bidder from the list and re_run the auction
      new_bidder_list = [self.clone_bidder(b) for b in self.bidder_list if b != bidder]
      sub_auction = VCG_sub_auction(new_bidder_list, self.total_objects)
      sub_auction.run_auction()

      # calculate VCG payment for each bidder
      bidder_payment = sub_auction.auction_revenue - (total_social_good - bidder.total_payment)
      bidder.set_vcg_payment(bidder_payment)

  def get_results(self):
    #[print(bidder.name + " gets " + str(round(bidder.curr_holdings / bidder.max_demand * 100, 2)) + "% for " + str(bidder.vcg_payment)) for bidder in self.bidder_list]
    [print(bidder.name + " gets " + str(round(bidder.curr_holdings / bidder.max_demand * 100, 2)) + " (" + str(bidder.curr_holdings) + " kwh)") for bidder in self.bidder_list]

class VCG_sub_auction:

  def __init__(self, bidder_list, total_objects):
    self.bidder_list = bidder_list
    self.total_objects = total_objects

    self.auction_revenue = 0

  def run_auction(self):
    while self.total_objects > 0: 
      ## calculate the bids for each bidder
      next_bids = [bidder.get_next_bid() for bidder in self.bidder_list]

      if(max(next_bids) == 0):
        break

      ## assign unit to the highest bidder.
      max_bid, max_bid_id = max(next_bids), next_bids.index(max(next_bids))
      self.bidder_list[max_bid_id].receive_object()
      self.auction_revenue += max_bid

      self.total_objects -= 1

    return


# each bidder is modeled by a linear equation bid = intercept - slope * curr_holdings
# i.e. bidder1 is the hospital whose demand is modeled by bid = 10 - 2 * curr_holdings, with a max of 5 

print("********** Q1 **********")

bidder1_q1 = Bidder("hospital", start_intercept=100, end_intercept=80, max_demand=1393)
bidder2_q1 = Bidder("grocery", start_intercept=70, end_intercept=40, max_demand=2739)
bidder3_q1 = Bidder("school", start_intercept=30, end_intercept=10, max_demand=449)
bidder4_q1 = Bidder("residential", start_intercept=50, end_intercept=20, max_demand=4336)
bidder5_q1 = Bidder("office", start_intercept=20, end_intercept=0, max_demand=691)

bidder_list = [bidder1_q1, bidder2_q1, bidder3_q1, bidder4_q1, bidder5_q1]

auction = VCG_Auction("q1", bidder_list, 4817)
auction.run_auction()
auction.get_results()

### AUCTION PERIOD 2
print("")
print("********** Q2 **********")

bidder1_q2 = Bidder("hospital", 120, 100, 3483)
bidder2_q2 = Bidder("grocery", 80, 50, 3423)
bidder3_q2 = Bidder("school", 10, 2, 135)
bidder4_q2 = Bidder("residential", 10, 0, 1445)
bidder5_q2 = Bidder("office", 20, 5, 1036)

bidder_list = [bidder1_q2, bidder2_q2, bidder3_q2, bidder4_q2, bidder5_q2]

auction_q2 = VCG_Auction("q2", bidder_list, 6021)
auction_q2.run_auction()
auction_q2.get_results()

### AUCTION PERIOD 3
print("")
print("********** Q3 **********")

bidder1_q3 = Bidder("hospital", 90, 80, 6038)
bidder2_q3 = Bidder("grocery", 60, 15, 4108)
bidder3_q3 = Bidder("school", 40, 10, 1346)
bidder4_q3 = Bidder("residential", 60, 0, 5058)
bidder5_q3 = Bidder("office", 20, 5, 1381)

bidder_list = [bidder1_q3, bidder2_q3, bidder3_q3, bidder4_q3, bidder5_q3]

auction_q3 = VCG_Auction("q3", bidder_list, 14450)
auction_q3.run_auction()
auction_q3.get_results()

### AUCTION PERIOD 4
print("")
print("********** Q4 **********")

bidder1_q2 = Bidder("hospital", 90, 80, 4180)
bidder2_q2 = Bidder("grocery", 65, 25, 3766)
bidder3_q2 = Bidder("school", 35, 15, 673)
bidder4_q2 = Bidder("residential", 70, 0, 5781)
bidder5_q2 = Bidder("office", 25, 10, 1036)

bidder_list = [bidder1_q2, bidder2_q2, bidder3_q2, bidder4_q2, bidder5_q2]

auction_q2 = VCG_Auction("q2", bidder_list, 12042)
auction_q2.run_auction()
auction_q2.get_results()

