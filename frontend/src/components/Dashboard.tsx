"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Plane, User, Phone, Mail, Clock, MessageSquare, AlertCircle, CheckCircle2 } from "lucide-react";
import ReactMarkdown from 'react-markdown';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

type Customer = {
  name: string;
  loyalty_tier: string;
  email: string;
  phone: string;
  travel_history?: {
    flights_last_12_months?: number;
    prior_complaints?: number;
    previous_complaint?: string;
    resolution?: string;
  };
};

type Booking = {
  flight: string;
  status: string;
  route: string;
  date: string;
  scheduled_departure: string;
  new_departure?: string;
  reason?: string;
};

export default function Dashboard() {
  const [bookingRef, setBookingRef] = useState("SK4821X");
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [booking, setBooking] = useState<Booking | null>(null);
  const [messages, setMessages] = useState<{ role: string, content: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [actions, setActions] = useState<string[]>([]);
  const [policies, setPolicies] = useState<string[]>([]);
  const [escalated, setEscalated] = useState(false);

  async function loadScenario(ref: string) {
    setBookingRef(ref);
    setMessages([]);
    setActions([]);
    setPolicies([]);
    setEscalated(false);
    
    // Fetch customer
    const cRes = await fetch(`${API_URL}/customer/${ref}`);
    if (cRes.ok) setCustomer(await cRes.json());
    
    // Fetch booking
    const bRes = await fetch(`${API_URL}/booking/${ref}`);
    if (bRes.ok) setBooking(await bRes.json());
  }

  useEffect(() => {
    // Initial scenario load is an intentional backend synchronization.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadScenario("SK4821X");
  }, []);

  const travelHistory = customer?.travel_history ?? {};

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMsg = { role: "user", content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);
    
    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, booking_reference: bookingRef })
      });
      const data = await res.json();
      
      setMessages(prev => [...prev, { role: "agent", content: data.response }]);
      setEscalated(data.escalated);
      if (data.actions_taken.length > 0) {
        setActions(prev => [...new Set([...prev, ...data.actions_taken])]);
      }
      if (data.policies_applied.length > 0) {
        setPolicies(prev => [...new Set([...prev, ...data.policies_applied])]);
      }
    } catch {
      setMessages(prev => [...prev, { role: "agent", content: "Sorry, connection error." }]);
    }
    setLoading(false);
  };

  return (
    <div className="flex min-h-screen w-full flex-col overflow-auto bg-[#f3f0e8] text-[#1b2942]">
      {/* Header */}
      <header 
        className="relative flex min-h-52 flex-wrap items-center justify-between gap-5 overflow-hidden bg-[#102a43] px-6 py-7 shadow-[0_8px_30px_rgba(16,42,67,0.18)] md:px-10"
        style={{
          backgroundImage: "url('/airline_banner.jpg')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-[#102a43]/95 via-[#173f5f]/85 to-[#e4b363]/30"></div>
        
        <div className="relative z-10 flex flex-col gap-3">
          <div className="flex items-center gap-3 text-white">
            <span className="grid size-11 place-items-center rounded-2xl bg-[#e4b363] text-[#102a43] shadow-lg">
              <Plane className="size-6" />
            </span>
            <div>
              <h1 className="text-2xl font-bold md:text-3xl">Altitude Resolutions</h1>
              <p className="mt-2 text-xs font-bold uppercase tracking-[0.18em] text-[#e4b363]">Operations desk · Live</p>
            </div>
          </div>
          <p className="max-w-md text-base font-medium leading-relaxed text-slate-200">AI-assisted decisions for calm, consistent customer care.</p>
        </div>

        <div className="relative z-10 flex w-full flex-wrap gap-2 rounded-2xl border border-white/20 bg-[#102a43]/50 p-2 backdrop-blur-md md:w-auto">
          <Button variant="secondary" className={bookingRef === "SK4821X" ? "bg-[#e4b363] text-[#102a43] hover:bg-[#efc77f]" : "bg-[#f7f4ec] text-[#173f5f] hover:bg-white"} size="sm" onClick={() => loadScenario("SK4821X")}>
            Priya · Cancelled
          </Button>
          <Button variant="secondary" className={bookingRef === "TR1190B" ? "bg-[#e4b363] text-[#102a43] hover:bg-[#efc77f]" : "bg-[#f7f4ec] text-[#173f5f] hover:bg-white"} size="sm" onClick={() => loadScenario("TR1190B")}>
            Arvind · 4h delay
          </Button>
          <Button variant="secondary" className={bookingRef === "WL7742" ? "bg-[#e4b363] text-[#102a43] hover:bg-[#efc77f]" : "bg-[#f7f4ec] text-[#173f5f] hover:bg-white"} size="sm" onClick={() => loadScenario("WL7742")}>
            Meher · 6h delay
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <div className="grid flex-1 gap-4 p-4 md:p-6 xl:grid-cols-[minmax(220px,280px)_minmax(420px,1fr)_minmax(220px,280px)]">
        
        {/* Left Sidebar - Customer Info */}
        <div className="flex flex-col gap-4">
          <Card className="dashboard-card border-[#d9d2c3] bg-[#fbfaf6] shadow-sm">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center gap-2 text-xl">
                <span className="grid size-8 place-items-center rounded-lg bg-[#dcebed] text-[#176b75]"><User className="size-4"/></span> Customer Profile
              </CardTitle>
            </CardHeader>
            <CardContent className="text-base leading-relaxed">
              {customer ? (
                <div className="flex flex-col gap-2">
                  <p><strong>Name:</strong> {customer.name}</p>
                  <p>
                    <strong>Tier:</strong> <Badge variant={customer.loyalty_tier === 'Gold' ? 'default' : 'secondary'}>{customer.loyalty_tier}</Badge>
                  </p>
                  <p className="flex items-center gap-2"><Mail className="w-4 h-4"/> {customer.email}</p>
                  <p className="flex items-center gap-2"><Phone className="w-4 h-4"/> {customer.phone}</p>
                  <div className="mt-4 border-t pt-4">
                    <p className="font-semibold mb-2">Travel History</p>
                    <p>Flights (12m): {travelHistory.flights_last_12_months ?? "N/A"}</p>
                    <p>Prior Complaints: {travelHistory.prior_complaints ?? "N/A"}</p>
                    {travelHistory.previous_complaint && (
                      <p className="text-muted-foreground mt-1">
                        Last issue: {travelHistory.previous_complaint} {travelHistory.resolution ? `(${travelHistory.resolution})` : ""}
                      </p>
                    )}
                  </div>
                </div>
              ) : (
                <p className="text-muted-foreground">Select a scenario above.</p>
              )}
            </CardContent>
          </Card>

          <Card className="dashboard-card border-[#d9d2c3] bg-[#fbfaf6] shadow-sm [animation-delay:100ms]">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center gap-2 text-xl">
                <span className="grid size-8 place-items-center rounded-lg bg-[#e8efdf] text-[#527343]"><AlertCircle className="size-4"/></span> Agent Activity
              </CardTitle>
            </CardHeader>
            <CardContent className="text-base leading-relaxed">
               <ul className="space-y-2">
                 <li className="flex items-center gap-2 text-green-600"><CheckCircle2 className="w-4 h-4"/> Customer verified</li>
                 <li className="flex items-center gap-2 text-green-600"><CheckCircle2 className="w-4 h-4"/> Booking retrieved</li>
                 {actions.map((act, i) => (
                    <li key={i} className="flex items-center gap-2 text-blue-600"><CheckCircle2 className="w-4 h-4"/> Executed: {act}</li>
                 ))}
                 {escalated && (
                    <li className="flex items-center gap-2 text-red-600"><AlertCircle className="w-4 h-4"/> Escalation Required</li>
                 )}
               </ul>
            </CardContent>
          </Card>
        </div>

        {/* Center - Chat Interface */}
        <Card className="dashboard-card flex min-h-[560px] flex-col overflow-hidden border-[#d9d2c3] bg-[#fbfaf6] shadow-[0_12px_30px_rgba(27,41,66,0.08)] [animation-delay:150ms] xl:min-h-0">
          <CardHeader className="border-b border-[#e6dfd2] bg-[#f7f4ec] pb-4">
            <CardTitle className="flex items-center gap-2 text-xl">
              <span className="grid size-8 place-items-center rounded-lg bg-[#173f5f] text-white"><MessageSquare className="size-4" /></span> Agent Workspace
            </CardTitle>
          </CardHeader>
          <ScrollArea className="min-h-0 flex-1 p-5">
            <div className="flex flex-col gap-4">
              {messages.length === 0 ? (
                <div className="flex min-h-64 flex-col items-center justify-center gap-3 text-center text-[#687484]">
                  <span className="grid size-14 place-items-center rounded-full bg-[#e8efdf] text-[#527343]"><MessageSquare className="size-6" /></span>
                  <p className="font-medium">Select a scenario and start the conversation.</p>
                </div>
              ) : (
                messages.map((m, i) => (
                  <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] rounded-lg p-3 ${
                      m.role === 'user' ? 'bg-[#173f5f] text-white shadow-sm' : 'border border-[#e2dbcf] bg-white text-[#1b2942] shadow-sm'
                    }`}>
                      <div className="prose prose-sm dark:prose-invert">
                        <ReactMarkdown>{m.content}</ReactMarkdown>
                      </div>
                    </div>
                  </div>
                ))
              )}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-slate-100 border rounded-lg p-3 text-slate-500 flex items-center gap-2">
                    <span className="animate-pulse">●</span>
                    <span className="animate-pulse delay-75">●</span>
                    <span className="animate-pulse delay-150">●</span>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
          <div className="border-t border-[#e6dfd2] bg-[#f7f4ec] p-4">
            <form onSubmit={e => { e.preventDefault(); sendMessage(); }} className="flex gap-2">
              <Input 
                value={input} 
                onChange={(e) => setInput(e.target.value)} 
                placeholder="Type customer request here..."
                className="flex-1"
                disabled={loading || !customer}
              />
              <Button type="submit" className="bg-[#d8844b] text-white hover:bg-[#bd6e38]" disabled={loading || !input.trim() || !customer}>
                Send
              </Button>
            </form>
          </div>
        </Card>

        {/* Right Sidebar - Flight & Policy */}
        <div className="flex flex-col gap-4">
          <Card className="dashboard-card border-[#d9d2c3] bg-[#fbfaf6] shadow-sm [animation-delay:200ms]">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center gap-2 text-xl">
                <span className="grid size-8 place-items-center rounded-lg bg-[#f5e4c5] text-[#a46727]"><Plane className="size-4"/></span> Flight Status
              </CardTitle>
            </CardHeader>
            <CardContent className="text-base leading-relaxed">
              {booking ? (
                <div className="flex flex-col gap-2">
                  <div className="flex items-center justify-between rounded-xl bg-[#f1ede4] p-3">
                    <span className="text-xl font-bold">{booking.flight}</span>
                    <Badge variant={booking.status === 'Cancelled' ? 'destructive' : 'outline'}>
                      {booking.status}
                    </Badge>
                  </div>
                  <p className="font-medium mt-2">{booking.route}</p>
                  <p className="flex items-center gap-2"><Clock className="w-4 h-4"/> {booking.date} @ {booking.scheduled_departure}</p>
                  {booking.new_departure && (
                    <p className="text-red-600">New Departure: {booking.new_departure}</p>
                  )}
                  {booking.reason && (
                    <p className="text-muted-foreground italic">Reason: {booking.reason}</p>
                  )}
                </div>
              ) : (
                <p className="text-muted-foreground">Select a scenario above.</p>
              )}
            </CardContent>
          </Card>

          <Card className="dashboard-card border-[#d9d2c3] bg-[#fbfaf6] shadow-sm [animation-delay:250ms]">
            <CardHeader className="pb-2">
              <CardTitle className="flex items-center gap-2 text-xl">
                <span className="grid size-8 place-items-center rounded-lg bg-[#f5e4c5] text-[#a46727]"><AlertCircle className="size-4"/></span> Policy Applied
              </CardTitle>
            </CardHeader>
            <CardContent className="text-base leading-relaxed">
              {policies.length > 0 ? (
                <ul className="list-disc pl-4 space-y-1">
                  {policies.map((p, i) => <li key={i} className="font-semibold">{p}</li>)}
                </ul>
              ) : (
                <p className="text-muted-foreground">No policies triggered yet.</p>
              )}
            </CardContent>
          </Card>
        </div>
        
      </div>
    </div>
  );
}
